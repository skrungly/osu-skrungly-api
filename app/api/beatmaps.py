from flask import abort
from flask_restx import Resource

from app import db, models
from app.api import api

map_namespace = api.namespace(
    name="maps",
    description="retreive basic map info",
)

set_namespace = api.namespace(
    name="mapsets",
    description="retreive basic mapset info",
)


beatmap_schema = models.BeatmapSchema()


@set_namespace.route("/<int:set_id>")
class BeatmapSetAPI(Resource):
    def get(self, set_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM maps WHERE set_id = %s", (set_id,))
            mapset_data = cursor.fetchall()
            db.commit()

        return beatmap_schema.dump(mapset_data, many=True) or abort(404)


@map_namespace.route("/<int:map_id>")
class BeatmapAPI(Resource):
    def get(self, map_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM maps WHERE id = %s", (map_id,))
            map_data = cursor.fetchone()
            db.commit()

        return beatmap_schema.dump(map_data) or abort(404)
