from flask_restx import Resource

from app import db, models
from app.api import api

namespace = api.namespace(
    name="stats",
    description="retrieve global server stats",
)

global_stats_schema = models.GlobalStatsSchema()


@namespace.route("")
class GlobalStatsAPI(Resource):
    def get(self):
        stats = {}

        db.ping()
        with db.cursor() as cursor:
            for stat_name in global_stats_schema.fields:
                cursor.execute(f"SELECT SUM({stat_name}) FROM stats")
                stats[stat_name] = cursor.fetchone()[f"SUM({stat_name})"]
                db.commit()

        return global_stats_schema.dump(stats)
