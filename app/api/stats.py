from flask_restx import Resource

from app import db, models
from app.api import api

namespace = api.namespace(
    name="stats",
    description="retreive global server stats",
)


@namespace.route("")
class GlobalStatsAPI(Resource):
    @api.marshal_with(models.global_stats_model)
    def get(self):
        stats = {}

        db.ping()
        with db.cursor() as cursor:
            for stat_name in models.global_stats_model:
                cursor.execute(f"SELECT SUM({stat_name}) FROM stats")
                stats[stat_name] = cursor.fetchone()[f"SUM({stat_name})"]
                db.commit()

        return stats
