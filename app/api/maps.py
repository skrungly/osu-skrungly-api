from flask import abort, request, send_file
from flask_restx import Resource

from app import db, models
from app.api import api
from app.rates import regenerate_osz_with_rates
from app.utils import fetch_beatmap_osz

namespace = api.namespace(
    name="maps",
    description="retrieve basic map info",
)

beatmap_schema = models.BeatmapSchema()
map_options_schema = models.BeatmapsOptionsSchema()


def _fetch_map_data(map_id):
    db.ping()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM maps WHERE id = %s", (map_id,))
        return cursor.fetchone()


@namespace.route("/<int:map_id>")
class BeatmapAPI(Resource):
    def get(self, map_id):
        map_data = _fetch_map_data(map_id)
        if not map_data:
            return {"message": "map does not exist in the database"}, 404

        return beatmap_schema.dump(map_data)


@namespace.route("/<int:map_id>/download")
class BeatmapDownloadAPI(Resource):
    def get(self, map_id):
        rates = request.args.getlist("rate")
        models.BeatmapRateDownloadSchema().validate({"rate": rates})

        map_data = _fetch_map_data(map_id)
        if not map_data:
            return {"message": "map does not exist in the database"}, 404

        try:
            osz_buffer = fetch_beatmap_osz(map_data["set_id"])
        except RuntimeError as e:
            # details should be provided in the error.
            return {"message": e.args[0]}, 422

        if osz_buffer is None:
            return {"message": "unable to fetch map from any mirrors"}, 422

        if rates:
            try:
                osz_buffer = regenerate_osz_with_rates(
                    osz_buffer,
                    map_data["filename"],
                    rates,
                )
            except FileNotFoundError:
                return {"message": "rate change service is unavailable"}, 503

            except RuntimeError as e:
                return {"message": e.args[0]}, 500

        rates_info = f" (+ {', '.join(rates)})" if rates else ""
        download_name = (
            f"{map_data['set_id']} "
            f"{map_data['artist']} - {map_data['title']}"
            f"{rates_info}.osz"
        )

        return send_file(
            osz_buffer,
            download_name=download_name,
            mimetype="application/octet-stream"
        )


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
                {filter_query} AND s.mode = m.mode
                GROUP BY m.md5
                ORDER BY popularity DESC, m.diff DESC
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
