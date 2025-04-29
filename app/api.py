from flask import abort
from flask_restful import Api, reqparse, Resource

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


class PlayerAPI(Resource):
    def get(self, user_id):
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, safe_name, priv, country, creation_time, "
                "  latest_activity, preferred_mode, userpage_content "
                "FROM users WHERE id = %s",
                (user_id,)
            )

            player_data = cursor.fetchone()
            if not player_data:
                abort(404)

            player_data["stats"] = {}

            cursor.execute("SELECT * FROM stats WHERE id = %s", user_id)
            for stats in cursor.fetchall():
                player_data["stats"][stats["mode"]] = stats

        return player_data

    def put(self, user_id):
        ...


class PlayerNameAPI(PlayerAPI):
    @staticmethod
    def _id_from_name(username):
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE name = %s", username)
            user_id = cursor.fetchone()
            if not user_id:
                abort(404)

        return user_id["id"]

    def get(self, username):
        return super().get(self._id_from_name(username))

    def put(self, username):
        return super().put(self._id_from_name(username))


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
            cursor.execute(
                "SELECT u.id, u.name, s.pp, s.plays, s.tscore, s.rscore "
                "FROM users u INNER JOIN stats s "
                "ON u.id = s.id "
                "WHERE s.mode = %s && s.plays != 0 "
                f"ORDER BY s.{args['sort']} DESC "
                "LIMIT %s OFFSET %s",
                (args["mode"], args["limit"], args["limit"] * args["page"])
            )

            return cursor.fetchall()


api.add_resource(PlayerNameAPI, "/players/<username>", endpoint="player_name")
api.add_resource(PlayerAPI, "/players/<int:user_id>", endpoint="player_id")
api.add_resource(LeaderboardAPI, "/leaderboard", endpoint="leaderboard")
