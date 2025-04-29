from flask import abort
from flask_restx import Api, reqparse, Resource

from app import app, db

api = Api(app)


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
    def get(self, id_or_name):
        identifier = "id" if id_or_name.isdigit() else "name"

        with db.cursor() as cursor:
            cursor.execute(f"""
                SELECT id, name, safe_name, priv, country, creation_time,
                  latest_activity, preferred_mode, userpage_content
                FROM users WHERE {identifier} = %s
                """, (id_or_name,)
            )

            player_data = cursor.fetchone()
            if not player_data:
                abort(404)

            cursor.execute(
                "SELECT * FROM stats WHERE id = %s", player_data["id"]
            )

            player_data["stats"] = {}
            for stats in cursor.fetchall():
                player_data["stats"][stats["mode"]] = stats

        return player_data

    def put(self, user_id):
        ...


@api.route("/leaderboard")
class LeaderboardAPI(Resource):
    def __init__(self):
        self.reqparse = PaginatedRequestParser()
        self.reqparse.add_argument("sort", type=str, default="pp")
        self.reqparse.add_argument("mode", type=int, required=True)
        super().__init__()

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
