from flask import abort, request
from flask_restx import Resource

from app import db, models
from app.api import api

namespace = api.namespace(
    name="maps",
    description="retrieve basic map info",
)

beatmap_schema = models.BeatmapSchema()
map_options_schema = models.BeatmapsOptionsSchema()


@namespace.route("/<int:map_id>")
class BeatmapAPI(Resource):
    def get(self, map_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM maps WHERE id = %s", (map_id,))
            map_data = cursor.fetchone()

        return beatmap_schema.dump(map_data) or abort(404)


@namespace.route("")
class BeatmapQueryAPI(Resource):
    def get(self):
        args = map_options_schema.load(request.args)

        # handle filtering options before sorting options because
        # we need these first (i.e. if sorting by popularity)
        filter_fields = []
        filter_values = []

        for filter_by in ("frozen", "mode", "set_id"):
            if filter_by in args:
                filter_fields.append(f"m.{filter_by} = %s")
                filter_values.append(args[filter_by])

        status = args.get("status", "all")
        status_values = map_options_schema._STATUS_ALIASES[status]
        filter_fields.append(
            "(" + " OR ".join(f"m.status = {s}" for s in status_values) + ")"
        )

        filter_query = ""
        if filter_fields:
            filter_query = "WHERE " + " AND ".join(filter_fields)

        # now figure out sorting options, including special cases
        sort_field = map_options_schema._SORT_OPTIONS[args["sort"]]

        if sort_field is not None:  # just basic sorting by key
            select_query = f"""
                SELECT m.* FROM maps m
                {filter_query}
                ORDER BY {sort_field} DESC
                LIMIT %s OFFSET %s
                """

        elif args["sort"] == "popular":  # requires special handling!
            # we want to count how many different players are on the
            # leaderboard, which requires joining by best scores.
            if not filter_query:
                filter_query = "WHERE s.status = 2"
            else:
                filter_query += " AND s.status = 2"

            select_query = f"""
                SELECT m.*, count(s.map_md5) AS popularity FROM maps m
                LEFT JOIN scores s ON m.md5 = s.map_md5
                {filter_query}
                GROUP BY m.md5
                ORDER BY popularity DESC
                LIMIT %s OFFSET %s
                """
        else:
            abort(500)  # this should not be reachable!

        db.ping()
        with db.cursor() as cursor:
            offset = args["limit"] * args["page"]

            cursor.execute(
                select_query,
                (*filter_values, args["limit"], offset)
            )

            fetched_data = cursor.fetchall()

        return models.BeatmapSchema().dump(fetched_data, many=True)
