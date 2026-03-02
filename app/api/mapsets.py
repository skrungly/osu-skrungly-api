from flask_restx import Resource

from app import db, models
from app.api import api
from app.rates import generate_osz_with_rates

namespace = api.namespace(
    name="mapsets",
    description="retrieve basic mapset info",
)


def _fetch_mapset_data(set_id):
    db.ping()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM maps WHERE set_id = %s", (set_id,))
        return cursor.fetchall()


@namespace.route("/<int:set_id>")
class BeatmapSetAPI(Resource):
    def get(self, set_id):
        mapset_data = _fetch_mapset_data(set_id)
        if not mapset_data:
            return {"message": "mapset does not exist in the database"}, 404

        return models.BeatmapSchema().dump(mapset_data, many=True)


@namespace.route("/<int:set_id>/download")
class BeatmapSetDownloadAPI(Resource):
    def get(self, set_id):
        mapset_data = _fetch_mapset_data(set_id)
        if not mapset_data:
            return {"message": "mapset does not exist in the database"}, 404

        task = generate_osz_with_rates.delay(set_id)
        return {"task": task.id}, 202
