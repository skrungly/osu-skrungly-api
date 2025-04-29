from flask import abort
from flask_restful import Api, Resource

from app import app, db

api = Api(app)


class PlayerAPI(Resource):
    def get(self, user_id):
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, safe_name, priv, country, creation_time, "
                "  latest_activity, preferred_mode, userpage_content "
                "FROM users WHERE id=(%s)",
                (user_id,)
            )

            player_data = cursor.fetchone()
            if not player_data:
                abort(404)

            player_data["stats"] = {}

            cursor.execute("SELECT * FROM stats WHERE id=(%s)", user_id)
            for stats in cursor.fetchall():
                player_data["stats"][stats["mode"]] = stats

        return player_data

    def put(self, user_id):
        ...


class PlayerNameAPI(PlayerAPI):
    @staticmethod
    def _id_from_name(username):
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE name=(%s)", username)
            user_id = cursor.fetchone()
            if not user_id:
                abort(404)

        return user_id["id"]

    def get(self, username):
        return super().get(self._id_from_name(username))

    def put(self, username):
        return super().put(self._id_from_name(username))


class PlayerListAPI(Resource):
    def get(self):
        ...


api.add_resource(PlayerNameAPI, "/players/<username>", endpoint="player_name")
api.add_resource(PlayerAPI, "/players/<int:user_id>", endpoint="player_id")
api.add_resource(PlayerListAPI, "/players", endpoint="players")
