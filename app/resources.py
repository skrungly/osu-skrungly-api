from flask_restful import Resource

from app import db


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
            player_data["stats"] = {}

            cursor.execute("SELECT * FROM stats WHERE id=(%s)", user_id)
            for stats in cursor.fetchall():
                player_data["stats"][stats["mode"]] = stats

        return player_data

    def put(self, user_id):
        ...


class PlayerListAPI(Resource):
    def get(self):
        ...
