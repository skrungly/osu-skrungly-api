import functools
from io import BytesIO

from flask import request, send_file
from flask_restx import Resource

from app import db, models, replay, skins
from app.api import api

namespace = api.namespace(
    name="scores",
    description="directly retrieve score-related info",
)

beatmap_schema = models.BeatmapSchema()
player_schema = models.PlayerSchema()
score_schema = models.ScoreSchema()
score_options_schema = models.ScoresOptionsSchema()


def resolve_score_data(api_method):
    @functools.wraps(api_method)
    def _get_score_data(api, score_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM scores WHERE id = %s", (score_id,))
            score_data = cursor.fetchone()

            if not score_data:
                return {"message": "score not found"}, 404

            cursor.execute(
                "SELECT * FROM maps WHERE md5 = %s", (score_data["map_md5"])
            )
            map_data = cursor.fetchone()

            cursor.execute(
                "SELECT * FROM users WHERE id = %s", (score_data["userid"])
            )
            player_data = cursor.fetchone()

        return api_method(api, score_data, map_data, player_data)

    return _get_score_data


@namespace.route("/<int:score_id>")
class ScoresAPI(Resource):
    @resolve_score_data
    def get(self, score_data, map_data, player_data):
        score_data["beatmap"] = map_data
        score_data["player"] = player_data
        return score_schema.dump(score_data)


@namespace.route("/<int:score_id>/screen")
class ScoresScreenAPI(Resource):
    @resolve_score_data
    def get(self, score_data, map_data, player_data):
        font_exists = replay.get_font_path(download=True)
        default_skin_exists = skins.check_for_default_skin(download=True)

        if not (font_exists and default_skin_exists):
            return {"message": "score screen service is unavailable"}, 503

        if score_data["status"] == 0:
            return {"message": "score was not completed"}, 404

        if map_data is None:
            return {"message": "map not found for that score"}, 404

        img = replay.get_replay_screen(
            score_data, map_data, player_data["name"], str(player_data["id"])
        )

        img_buffer = BytesIO()
        img.save(img_buffer, "PNG")
        img_buffer.seek(0)
        return send_file(img_buffer, mimetype="image/png")


@namespace.route("")
class ScoresQueryAPI(Resource):
    def get(self):
        args = score_options_schema.load(request.args)

        sort_field = score_options_schema._SORT_OPTIONS[args["sort"]]
        order_by_query = f"ORDER BY s.{sort_field} DESC"

        # begin with the simpler filter options
        filter_fields = []
        filter_values = []

        for filter_by in ("mods", "grade", "mode"):
            if filter_by in args:
                filter_fields.append(f"s.{filter_by} = %s")
                filter_values.append(args[filter_by])

        # now onto the slightly more involved filters
        if "beatmap" in args:
            if args["beatmap"].isdigit():
                filter_fields.append("m.id = %s")
            else:
                filter_fields.append("s.map_md5 = %s")

            filter_values.append(args["beatmap"])

        if "player" in args:
            if args["player"].isdigit():
                filter_fields.append("s.userid = %s")
            else:
                filter_fields.append("u.name = %s")

            filter_values.append(args["player"])

        # status is "passed" by default
        status = score_options_schema._STATUS_ALIASES[args["status"]]
        filter_fields.append(
            "(" + " OR ".join(f"s.status = {s}" for s in status) + ")"
        )

        # one more filter: if we're sorting by pp, we should only
        # return scores on pp-awarding maps (ranked or approved).
        if sort_field == "pp":
            filter_fields.append("(m.status = 2 OR m.status = 3)")

        filter_query = ""
        if filter_fields:
            filter_query = "WHERE " + " AND ".join(filter_fields)

        db.ping()
        with db.cursor() as cursor:
            offset = args["limit"] * args["page"]
            cursor.execute(f"""
                SELECT * FROM scores s
                INNER JOIN maps m ON s.map_md5 = m.md5
                INNER JOIN users u ON s.userid = u.id
                {filter_query}
                {order_by_query}
                LIMIT %s OFFSET %s
                """, (*filter_values, args["limit"], offset)
            )

            fetched_data = cursor.fetchall()

        # the data is a mix of map, score, and player properties,
        # which need to be separated to fit the score model
        scores = []
        for score_data in fetched_data:
            score = {}
            beatmap = {}
            player = {}
            for key, value in score_data.items():
                # if the key name matches a column in either model,
                # add it provisionally if it's not already there.
                if key in score_schema.fields and key not in score:
                    score[key] = value

                if key in beatmap_schema.fields and key not in beatmap:
                    beatmap[key] = value

                if key in player_schema.fields and key not in player:
                    player[key] = value

                # in the case of ambiguous keys, there will be a
                # prefix ("s." or "m.") which should take priority
                if key.startswith("s."):
                    score[key[2:]] = value

                elif key.startswith("m."):
                    beatmap[key[2:]] = value

                elif key.startswith("u."):
                    player[key[2:]] = value

            score["beatmap"] = beatmap
            score["player"] = player
            scores.append(score)

        return models.ScoreSchema().dump(scores, many=True)
