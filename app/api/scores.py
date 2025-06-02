import functools
from io import BytesIO

from flask import send_file
from flask_restx import Resource

from app import db, models, replay, skins
from app.api import api

namespace = api.namespace(
    name="scores",
    description="directly retrieve score-related info",
)

score_schema = models.ScoreSchema()


def resolve_score_and_map(api_method):
    @functools.wraps(api_method)
    def _get_score_and_map(api, score_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM scores WHERE id = %s", (score_id,))
            score_data = cursor.fetchone()

            if not score_data:
                return {"message": "score not found"}, 404

            cursor.execute(
                "SELECT * FROM maps WHERE md5 = %s", (score_data["map_md5"])
            )

            map_data = cursor.fetchone()

        return api_method(api, score_data, map_data)

    return _get_score_and_map


@namespace.route("/<int:score_id>")
class ScoresAPI(Resource):
    @resolve_score_and_map
    def get(self, score_data, map_data):
        score_data["beatmap"] = map_data
        return score_schema.dump(score_data)


@namespace.route("/<int:score_id>/screen")
class ScoresScreenAPI(Resource):
    @resolve_score_and_map
    def get(self, score_data, map_data):
        font_exists = replay.get_font_path(download=True)
        default_skin_exists = skins.check_for_default_skin(download=True)

        if not (font_exists and default_skin_exists):
            return {"message": "score screen service is unavailable"}, 503

        if score_data["status"] == 0:
            return {"message": "score was not completed"}, 404

        if map_data is None:
            return {"message": "map not found for that score"}, 404

        user_id = score_data["userid"]

        with db.cursor() as cursor:
            cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
            player_info = cursor.fetchone()

        if not player_info:
            return {"message": "player not found for that score"}, 404

        img = replay.get_replay_screen(
            score_data, map_data, player_info["name"], str(user_id)
        )

        img_buffer = BytesIO()
        img.save(img_buffer, "PNG")
        img_buffer.seek(0)
        return send_file(img_buffer, mimetype="image/png")
