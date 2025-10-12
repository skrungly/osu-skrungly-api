from flask import abort
from flask_restx import Resource

from app import db, models
from app.api import api

namespace = api.namespace(
    name="mapsets",
    description="retrieve basic mapset info",
)

beatmap_schema = models.BeatmapSchema()


@namespace.route("/<int:set_id>")
class BeatmapSetAPI(Resource):
    def get(self, set_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM maps WHERE set_id = %s", (set_id,))
            mapset_data = cursor.fetchall()

        return beatmap_schema.dump(mapset_data, many=True) or abort(404)
