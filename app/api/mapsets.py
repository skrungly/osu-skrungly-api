from flask import abort, send_file
from flask_restx import Resource

from app import db, models
from app.api import api
from app.utils import fetch_beatmap_osz

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


@namespace.route("/<int:set_id>/download")
class BeatmapSetDownloadAPI(Resource):
    def get(self, set_id):
        try:
            osz_buffer = fetch_beatmap_osz(set_id)
        except RuntimeError as e:
            # details should be provided in the error.
            return {"message": e.args[0]}, 422

        if osz_buffer is None:
            return {"message": "unable to fetch map from any mirrors"}, 422

        return send_file(
            osz_buffer,
            download_name=f"{set_id}.osz",
            mimetype="application/octet-stream"
        )
