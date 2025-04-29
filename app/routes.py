from flask import abort
from flask_restx import reqparse, Resource

from app import api, db, models


MODE_NAMES = {
    "osu": 0,
    "taiko": 1,
    "catch": 2,
    "mania": 3,
    "relax": 4,
}


def _resolve_player_id(id_or_name: str):
    if id_or_name.isdigit():
        return id_or_name

    with db.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE name = %s", (id_or_name,))
        return cursor.fetchone().get("id")


def _resolve_mode_id(id_or_name: str):
    if id_or_name.isdigit():
        return id_or_name

    return MODE_NAMES.get(id_or_name)


class PaginatedRequestParser(reqparse.RequestParser):
    def __init__(self, *args, max_limit=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_limit = max_limit

        self.add_argument("page", type=int, default=0)
        self.add_argument("limit", type=int, default=10)

    def parse_args(self, *args, **kwargs):
        req_args = super().parse_args(*args, **kwargs)

        if req_args["limit"] > self.max_limit:
            abort(422)

        return req_args


@api.route("/scores/<int:score_id>")
class ScoreAPI(Resource):
    @api.marshal_with(models.score_model)
    def get(self, score_id):
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM scores WHERE id = %s", (score_id,))
            score_data = cursor.fetchone() or abort(404)

            cursor.execute(
                "SELECT * FROM maps WHERE md5 = %s", (score_data["map_md5"])
            )

            score_data["beatmap"] = cursor.fetchone()

        return score_data


@api.route("/players/<id_or_name>")
class PlayerAPI(Resource):
    @api.marshal_with(models.player_model)
    def get(self, id_or_name):
        if not (player_id := _resolve_player_id(id_or_name)):
            abort(404)

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, safe_name, priv, country, creation_time,
                  latest_activity, preferred_mode, userpage_content
                FROM users WHERE id = %s
                """, (player_id,)
            )

            player_data = cursor.fetchone() or abort(404)

            cursor.execute("SELECT * FROM stats WHERE id = %s", (player_id,))
            player_data["stats"] = cursor.fetchall()

        return player_data

    def put(self, user_id):
        ...


@api.route("/players/<id_or_name>/stats")
class PlayerStatsAPI(Resource):
    def __init__(self, *args, **kwargs):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("mode", type=str, required=True)
        super().__init__(*args, **kwargs)

    @api.marshal_with(models.player_stats_model)
    def get(self, id_or_name):
        args = self.reqparse.parse_args()
        if not (mode_id := _resolve_mode_id(args["mode"])):
            abort(422)

        if not (player_id := _resolve_player_id(id_or_name)):
            abort(404)

        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM stats
                WHERE mode = %s and id = %s and plays > 0
                """, (mode_id, player_id),
            )

            return cursor.fetchone() or abort(404)


@api.route("/players/<id_or_name>/scores")
class PlayerScoresAPI(Resource):
    def __init__(self, *args, **kwargs):
        self.reqparse = PaginatedRequestParser()
        self.reqparse.add_argument("sort", type=str, default="pp")
        self.reqparse.add_argument("mode", type=str, required=True)
        super().__init__(*args, **kwargs)

    @api.marshal_with(models.score_model)
    def get(self, id_or_name):
        args = self.reqparse.parse_args()

        if not (mode_id := _resolve_mode_id(args["mode"])):
            abort(422)

        if not (player_id := _resolve_player_id(id_or_name)):
            abort(404)

        if args["sort"] == "pp":
            query = """
                SELECT m.*, s.* FROM scores s
                INNER JOIN maps m ON m.md5 = s.map_md5
                WHERE s.userid = %s AND s.mode = %s
                    AND s.status = 2 AND m.status = 2
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

        with db.cursor() as cursor:
            offset = args["limit"] * args["page"]
            cursor.execute(query, (player_id, mode_id, args["limit"], offset))
            score_and_beatmap = cursor.fetchall()

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


@api.route("/leaderboard")
class LeaderboardAPI(Resource):
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

            return cursor.fetchall()


@api.route("/mapsets/<int:set_id>")
class BeatmapSetAPI(Resource):
    @api.marshal_with(models.beatmap_model)
    def get(self, set_id):
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM maps WHERE set_id = %s", (set_id,))
            return cursor.fetchall() or abort(404)


@api.route("/maps/<int:map_id>")
class BeatmapAPI(Resource):
    @api.marshal_with(models.beatmap_model)
    def get(self, map_id):
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM maps WHERE id = %s", (map_id,))
            return cursor.fetchone() or abort(404)
