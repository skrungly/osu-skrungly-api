from flask import abort
from flask_restx import Resource

from app import db, models
from app.api import api

namespace = api.namespace(
    name="maps",
    description="retrieve basic map info",
)

beatmap_schema = models.BeatmapSchema()


@namespace.route("/<int:map_id>")
class BeatmapAPI(Resource):
    def get(self, map_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM maps WHERE id = %s", (map_id,))
            map_data = cursor.fetchone()

        return beatmap_schema.dump(map_data) or abort(404)
