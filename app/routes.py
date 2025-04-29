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


@api.route("/players/<id_or_name>")
class PlayerAPI(Resource):
    @api.marshal_with(models.player_model)
    def get(self, id_or_name):
        identifier = "id" if id_or_name.isdigit() else "name"

        with db.cursor() as cursor:
            cursor.execute(f"""
                SELECT id, name, safe_name, priv, country, creation_time,
                  latest_activity, preferred_mode, userpage_content
                FROM users WHERE {identifier} = %s
                """, (id_or_name,)
            )

            return cursor.fetchone() or abort(404)

    def put(self, user_id):
        ...


@api.route("/players/<id_or_name>/stats/<mode>")
class PlayerStatsAPI(Resource):
    @api.marshal_with(models.player_stats_model)
    def get(self, id_or_name, mode):
        if not mode.isdigit():
            mode = MODE_NAMES.get(mode) or abort(404)

        with db.cursor() as cursor:
            # find the player id if we're given a name
            if not id_or_name.isdigit():
                cursor.execute(
                    "SELECT id FROM users WHERE name = %s", (id_or_name,)
                )
                player_id = cursor.fetchone().get("id") or abort(404)
            else:
                player_id = id_or_name

            # now fetch the stats if the player has any
            cursor.execute("""
                SELECT * FROM stats
                WHERE mode = %s and id = %s and plays > 0
                """, (mode, player_id),
            )

            return cursor.fetchone() or abort(404)


@api.route("/leaderboard")
class LeaderboardAPI(Resource):
    def __init__(self, *args, **kwargs):
        self.reqparse = PaginatedRequestParser()
        self.reqparse.add_argument("sort", type=str, default="pp")
        self.reqparse.add_argument("mode", type=int, required=True)
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
