import functools
import hashlib

import bcrypt
from flask import abort, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from werkzeug.utils import secure_filename

from app import db, models, skins
from app.api import api
from app.utils import (
    OSK_DIR,
    resolve_mode_id,
    valid_password,
    valid_username,
)

namespace = api.namespace(
    name="players",
    description="players and associated info (stats, scores, etc.)",
)

player_schema = models.PlayerSchema()
player_stats_schema = models.PlayerStatsSchema()

beatmap_schema = models.BeatmapSchema()
leaderboard_schema = models.LeaderboardSchema()
score_schema = models.ScoreSchema()


def resolve_player_id(api_method):
    @functools.wraps(api_method)
    def _check_player_id(api, id_or_name):
        if id_or_name.isdigit():
            return api_method(api, int(id_or_name))

        db.ping()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE name = %s", (id_or_name,)
            )

            player_id = cursor.fetchone()
            db.commit()

        if player_id is not None:
            return api_method(api, player_id["id"])

        return {"message": f"player '{id_or_name}' does not exist."}, 404

    return _check_player_id


@namespace.route("")
class PlayerListAPI(Resource):
    def get(self):
        args = models.ModeListOptionsSchema().load(request.args)

        mode_id = resolve_mode_id(args["mode"])
        if mode_id is None:
            abort(422)

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

        return leaderboard_schema.dump(leaderboard_data, many=True)


@namespace.route("/<id_or_name>")
class PlayerAPI(Resource):
    @resolve_player_id
    def get(self, player_id):
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
        return player_schema.dump(player_data)

    @jwt_required()
    @resolve_player_id
    def put(self, player_id):
        # TODO: this could be a decorator in its own right:
        if str(player_id) != get_jwt_identity():
            abort(403)

        # TODO: maybe move validation to the schema itself
        args = player_schema.load(request.get_json())
        set_fields = {}

        # specifically check against None to allow for "" (empty)
        # so that we may return a more specific error response.
        if (new_name := args.get("name")) is not None:
            if not valid_username(new_name):
                abort(422)

            set_fields["name"] = new_name
            set_fields["safe_name"] = new_name.lower().replace(" ", "_")

        if (new_password := args.get("password")) is not None:
            if not valid_password(new_password):
                abort(422)

            pw_md5 = hashlib.md5(new_password.encode()).hexdigest().encode()
            set_fields["pw_bcrypt"] = bcrypt.hashpw(pw_md5, bcrypt.gensalt())

        if (new_userpage := args.get("userpage_content")) is not None:
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

        return "", 204


@namespace.route("/<id_or_name>/stats")
class PlayerStatsAPI(Resource):
    @resolve_player_id
    def get(self, player_id):
        args = models.PlayerStatsOptionsSchema().load(request.args)

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

        return player_stats_schema.dump(stats_data) or abort(404)


@namespace.route("/<id_or_name>/scores")
class PlayerScoresAPI(Resource):
    @resolve_player_id
    def get(self, player_id):
        args = models.ModeListOptionsSchema().load(request.args)

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
                if key in score_schema.fields and key not in score:
                    score[key] = value

                if key in beatmap_schema.fields and key not in beatmap:
                    beatmap[key] = value

                # in the case of ambiguous keys, there will be a
                # prefix ("s." or "m.") which should take priority
                if key.startswith("s."):
                    score[key[2:]] = value

                elif key.startswith("m."):
                    beatmap[key[2:]] = value

            score["beatmap"] = beatmap
            scores.append(score)

        return score_schema.dump(scores, many=True)


@namespace.route("/<id_or_name>/skin")
class PlayerSkinAPI(Resource):
    @resolve_player_id
    def get(self, player_id):
        archive_dir = OSK_DIR / str(player_id)
        if archive_dir.exists():
            # there should only be one file here
            for osk_file in archive_dir.iterdir():
                return send_file(archive_dir / osk_file.name)

        return {"message": "no skin found for that player."}, 404

    @jwt_required()
    @resolve_player_id
    def put(self, player_id):
        if str(player_id) != get_jwt_identity():
            abort(403)

        args = models.FileUploadSchema().load(request.files)
        osk_file = request.files["file"]
        file_name = secure_filename(args["file"].filename)

        try:
            skins.save_skin(osk_file, file_name, str(player_id))
        except RuntimeError:
            return {"message": "extracted skin exceeds size limit"}, 413

        return "", 204

    @jwt_required()
    @resolve_player_id
    def delete(self, player_id):
        if str(player_id) != get_jwt_identity():
            abort(403)

        skins.delete_skin(player_id)
        return "", 204
