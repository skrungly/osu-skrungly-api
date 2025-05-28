import hashlib

import bcrypt
from flask import abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import reqparse, Resource

from app import db, models
from app.api import api
from app.utils import (
    PaginatedRequestParser,
    resolve_mode_id,
    resolve_player_id,
    valid_password,
    valid_username,
)

namespace = api.namespace(
    name="players",
    description="players and associated info (stats, scores, etc.)",
)


@namespace.route("")
class PlayerListAPI(Resource):
    def __init__(self, *args, **kwargs):
        self.reqparse = PaginatedRequestParser()
        self.reqparse.add_argument("sort", type=str, default="pp")
        self.reqparse.add_argument("mode", type=str, required=True)
        super().__init__(*args, **kwargs)

    @api.marshal_with(models.leaderboard_model)
    def get(self):
        args = self.reqparse.parse_args()

        if args["sort"] not in ("pp", "plays", "tscore", "rscore"):
            abort(422)

        db.ping()
        with db.cursor() as cursor:
            offset = args["limit"] * args["page"]
            cursor.execute(f"""
                SELECT u.id, u.name, s.pp, s.plays, s.tscore, s.rscore
                FROM users u INNER JOIN stats s
                ON u.id = s.id
                WHERE s.mode = %s && s.plays != 0
                ORDER BY s.{args['sort']} DESC
                LIMIT %s OFFSET %s
                """, (args["mode"], args["limit"], offset)
            )

            leaderboard_data = cursor.fetchall()
            db.commit()

        return leaderboard_data


@namespace.route("/<id_or_name>")
class PlayerAPI(Resource):
    def __init__(self, *args, **kwargs):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("name", type=str)
        self.reqparse.add_argument("password", type=str)
        self.reqparse.add_argument("userpage_content", type=str)
        super().__init__(*args, **kwargs)

    @api.marshal_with(models.player_model)
    def get(self, id_or_name):
        if not (player_id := resolve_player_id(id_or_name)):
            abort(404)

        db.ping()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, safe_name, priv, country, creation_time,
                  latest_activity, preferred_mode, userpage_content
                FROM users WHERE id = %s
                """, (player_id,)
            )

            player_data = cursor.fetchone()
            if not player_data:
                db.commit()
                abort(404)

            cursor.execute("SELECT * FROM stats WHERE id = %s", (player_id,))
            stats_data = cursor.fetchall()
            db.commit()

        player_data["stats"] = stats_data
        return player_data

    @jwt_required()
    def put(self, id_or_name):
        if not (player_id := resolve_player_id(id_or_name)):
            abort(404)

        if str(player_id) != get_jwt_identity():
            abort(403)

        args = self.reqparse.parse_args()
        set_fields = {}

        # specifically check against None to allow for "" (empty)
        # so that we may return a more specific error response.
        if (new_name := args["name"]) is not None:
            if not valid_username(new_name):
                abort(422)

            set_fields["name"] = new_name
            set_fields["safe_name"] = new_name.lower().replace(" ", "_")

        if (new_password := args["password"]) is not None:
            if not valid_password(new_password):
                abort(422)

            pw_md5 = hashlib.md5(new_password.encode()).hexdigest().encode()
            set_fields["pw_bcrypt"] = bcrypt.hashpw(pw_md5, bcrypt.gensalt())

        if (new_userpage := args["userpage_content"]) is not None:
            if len(new_userpage) > 2048:
                abort(422)

            set_fields["userpage_content"] = new_userpage

        set_query = ", ".join(f"{key} = %({key})s" for key in set_fields)

        db.ping()
        with db.cursor() as cursor:
            query_args = set_fields | {"id": player_id}
            cursor.execute(
                f"UPDATE users SET {set_query} WHERE id = %(id)s", query_args
            )

            db.commit()

        # TODO: normalise this sort of response
        return {"success": True}


@namespace.route("/<id_or_name>/stats")
class PlayerStatsAPI(Resource):
    def __init__(self, *args, **kwargs):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("mode", type=str, required=True)
        super().__init__(*args, **kwargs)

    @api.marshal_with(models.player_stats_model)
    def get(self, id_or_name):
        args = self.reqparse.parse_args()

        if not (player_id := resolve_player_id(id_or_name)):
            abort(404)

        mode_id = resolve_mode_id(args["mode"])
        if mode_id is None:
            abort(422)

        db.ping()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM stats
                WHERE mode = %s and id = %s and plays > 0
                """, (mode_id, player_id),
            )

            stats_data = cursor.fetchone()
            db.commit()

        return stats_data or abort(404)


@namespace.route("/<id_or_name>/scores")
class PlayerScoresAPI(Resource):
    def __init__(self, *args, **kwargs):
        self.reqparse = PaginatedRequestParser()
        self.reqparse.add_argument("sort", type=str, default="pp")
        self.reqparse.add_argument("mode", type=str, required=True)
        super().__init__(*args, **kwargs)

    @api.marshal_with(models.score_model)
    def get(self, id_or_name):
        args = self.reqparse.parse_args()

        if not (player_id := resolve_player_id(id_or_name)):
            abort(404)

        mode_id = resolve_mode_id(args["mode"])
        if mode_id is None:
            abort(422)

        if args["sort"] == "pp":
            query = """
                SELECT m.*, s.* FROM scores s
                INNER JOIN maps m ON m.md5 = s.map_md5
                WHERE s.userid = %s AND s.mode = %s AND s.status = 2
                    AND (m.status = 2 OR m.status = 3)
                ORDER BY s.pp DESC
                LIMIT %s OFFSET %s
                """

        elif args["sort"] == "recent":
            query = """
                SELECT m.*, s.* FROM scores s
                INNER JOIN maps m ON m.md5 = s.map_md5
                WHERE s.userid = %s AND s.mode = %s AND s.status != 0
                ORDER BY s.play_time DESC
                LIMIT %s OFFSET %s
                """
        else:
            abort(422)

        db.ping()
        with db.cursor() as cursor:
            offset = args["limit"] * args["page"]
            cursor.execute(query, (player_id, mode_id, args["limit"], offset))
            score_and_beatmap = cursor.fetchall()
            db.commit()

        # the resulting data is a mix of map and score properties,
        # which need to be separated to fit the score model
        scores = []
        for score_data in score_and_beatmap:
            score = {}
            beatmap = {}
            for key, value in score_data.items():
                # if the key name matches a column in either model,
                # add it provisionally if it's not already there.
                if key in models.score_model and key not in score:
                    score[key] = value

                if key in models.beatmap_model and key not in beatmap:
                    beatmap[key] = value

                # in the case of ambiguous keys, there will be a
                # prefix ("s." or "m.") which should take priority
                if key.startswith("s."):
                    score[key[2:]] = value

                elif key.startswith("m."):
                    beatmap[key[2:]] = value

            score["beatmap"] = beatmap
            scores.append(score)

        return scores
