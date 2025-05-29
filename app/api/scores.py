from flask import abort
from flask_restx import Resource

from app import db, models
from app.api import api

namespace = api.namespace(
    name="scores",
    description="directly retreive score-related info",
)

score_schema = models.ScoreSchema()


@namespace.route("/scores/<int:score_id>")
class ScoresAPI(Resource):
    def get(self, score_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM scores WHERE id = %s", (score_id,))
            score_data = cursor.fetchone()

            if not score_data:
                db.commit()
                abort(404)

            cursor.execute(
                "SELECT * FROM maps WHERE md5 = %s", (score_data["map_md5"])
            )

            map_data = cursor.fetchone()
            db.commit()

        score_data["beatmap"] = map_data
        return score_schema.dump(score_data)
