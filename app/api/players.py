import functools
import hashlib

import bcrypt
from flask import abort, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps

from app import app, db, models, skins
from app.api import api

namespace = api.namespace(
    name="players",
    description="players and associated info (stats, scores, etc.)",
)

player_schema = models.PlayerSchema()
player_edit_schema = models.PlayerEditOptionsSchema()
player_stats_schema = models.PlayerStatsSchema()

beatmap_schema = models.BeatmapSchema()
leaderboard_schema = models.LeaderboardSchema()
score_schema = models.ScoreSchema()


def resolve_player_id(api_method):
    @functools.wraps(api_method)
    def _check_player_id(api, id_or_name):
        if id_or_name.isdigit():
            return api_method(api, int(id_or_name))

        db.ping()
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE name = %s", (id_or_name,)
            )

            player_id = cursor.fetchone()

        if player_id is not None:
            return api_method(api, player_id["id"])

        return {"message": f"player '{id_or_name}' does not exist."}, 404

    return _check_player_id


@namespace.route("")
class PlayerListAPI(Resource):
    def get(self):
        args = models.PlayerListOptionsSchema().load(request.args)

        if args["sort"] not in ("pp", "plays", "tscore", "rscore"):
            abort(422)

        db.ping()
        with db.cursor() as cursor:
            offset = args["limit"] * args["page"]
            cursor.execute(f"""
                SELECT u.id, u.name, s.pp, s.plays, s.tscore, s.rscore
                FROM users u INNER JOIN stats s
                ON u.id = s.id
                WHERE s.mode = %s && s.plays != 0
                ORDER BY s.{args['sort']} DESC
                LIMIT %s OFFSET %s
                """, (args["mode"], args["limit"], offset)
            )

            leaderboard_data = cursor.fetchall()
        return leaderboard_schema.dump(leaderboard_data, many=True)


@namespace.route("/<id_or_name>")
class PlayerAPI(Resource):
    @resolve_player_id
    def get(self, player_id):
        db.ping()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, safe_name, priv, country, creation_time,
                  latest_activity, preferred_mode, userpage_content
                FROM users WHERE id = %s
                """, (player_id,)
            )

            player_data = cursor.fetchone()
            if not player_data:
                abort(404)

            cursor.execute("SELECT * FROM stats WHERE id = %s", (player_id,))
            stats_data = cursor.fetchall()

        player_data["stats"] = stats_data
        return player_schema.dump(player_data)

    @jwt_required()
    @resolve_player_id
    def put(self, player_id):
        # TODO: this could be a decorator in its own right:
        if str(player_id) != get_jwt_identity():
            abort(403)

        # TODO: maybe move validation to the schema itself
        args = player_edit_schema.load(request.get_json())
        new_fields = {}

        # specifically check against None to allow for "" (empty)
        # so that we may return a more specific error response.
        if (new_name := args.get("name")) is not None:
            new_fields["name"] = new_name
            new_fields["safe_name"] = new_name.lower().replace(" ", "_")

        if (new_password := args.get("password")) is not None:
            pw_md5 = hashlib.md5(new_password.encode()).hexdigest().encode()
            new_fields["pw_bcrypt"] = bcrypt.hashpw(pw_md5, bcrypt.gensalt())

        if (new_userpage := args.get("userpage_content")) is not None:
            new_fields["userpage_content"] = new_userpage

        if not new_fields:
            return "", 204

        set_query = ", ".join(f"{key} = %({key})s" for key in new_fields)

        db.ping()
        with db.cursor() as cursor:
            query_args = new_fields | {"id": player_id}
            cursor.execute(
                f"UPDATE users SET {set_query} WHERE id = %(id)s", query_args
            )

        return "", 204


@namespace.route("/<id_or_name>/stats")
class PlayerStatsAPI(Resource):
    @resolve_player_id
    def get(self, player_id):
        args = models.PlayerStatsOptionsSchema().load(request.args)

        db.ping()
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM stats
                WHERE mode = %s and id = %s
                """, (args["mode"], player_id),
            )

            stats_data = cursor.fetchone()

        return player_stats_schema.dump(stats_data)


@namespace.route("/<id_or_name>/skin")
class PlayerSkinAPI(Resource):
    @resolve_player_id
    def get(self, player_id):
        archive_dir = app.osk_dir / str(player_id)
        if archive_dir.exists():
            # there should only be one file here
            for osk_file in archive_dir.iterdir():
                return send_file(archive_dir / osk_file.name)

        return {"message": "no skin found for that player."}, 404

    @jwt_required()
    @resolve_player_id
    def put(self, player_id):
        if str(player_id) != get_jwt_identity():
            abort(403)

        args = models.FileUploadSchema().load(request.files)
        osk_file = request.files["file"]
        file_name = secure_filename(args["file"].filename)

        try:
            skins.save_skin(osk_file, file_name, str(player_id))
        except RuntimeError:
            return {"message": "extracted skin exceeds size limit"}, 413

        return "", 204

    @jwt_required()
    @resolve_player_id
    def delete(self, player_id):
        if str(player_id) != get_jwt_identity():
            abort(403)

        skins.delete_skin(str(player_id))
        return "", 204


@namespace.route("/<id_or_name>/banner")
class PlayerBannerAPI(Resource):
    BANNER_SIZE = (1360, 230)

    @resolve_player_id
    def get(self, player_id):
        banner_path = app.banners_dir / f"{player_id}.jpg"

        if not banner_path.exists():
            return {"message": "no banner found for that player."}, 404

        return send_file(banner_path)

    @jwt_required()
    @resolve_player_id
    def put(self, player_id):
        if str(player_id) != get_jwt_identity():
            abort(403)

        banner_file = request.files["file"]

        banner_path = app.banners_dir / f"{player_id}.jpg"
        if banner_path.exists():
            banner_path.unlink()

        # crop and resize the image to a better banner size
        original_img = Image.open(banner_file)
        banner_img = ImageOps.fit(original_img, self.BANNER_SIZE)
        banner_img.save(banner_path, format='JPEG', subsampling=0, quality=95)
        return "", 204

    @jwt_required()
    @resolve_player_id
    def delete(self, player_id):
        if str(player_id) != get_jwt_identity():
            abort(403)

        banner_path = app.banners_dir / f"{player_id}.jpg"
        if banner_path.exists():
            banner_path.unlink()
            return "", 204

        return {"message": "no banner found for that player."}, 404
