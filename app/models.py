import hashlib
from dataclasses import dataclass

import bcrypt
from flask_restx.fields import DateTime, Float, Integer, Nested, String

from app import api, db


@dataclass
class User:
    id: int

    @classmethod
    def authenticate(cls, username=None, password=None):
        if not username or not password:
            return None

        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, pw_bcrypt FROM users WHERE name = %s", (username,)
            )

            user_info = cursor.fetchone()
            if not user_info:
                return None

        # the bancho.py service uses a double hash
        pw_md5 = hashlib.md5(password.encode()).hexdigest().encode()
        if not bcrypt.checkpw(pw_md5, user_info["pw_bcrypt"].encode()):
            return None

        return cls(user_info["id"])


global_stats_model = api.model("GlobalStats", {
    "tscore": Integer,
    "rscore": Integer,
    "pp": Integer,
    "plays": Integer,
    "playtime": Integer,
    "total_hits": Integer,
})

player_stats_model = api.model("PlayerStats", {
    "id": Integer,
    "mode": Integer,
    "tscore": Integer,
    "rscore": Integer,
    "pp": Integer,
    "plays": Integer,
    "playtime": Integer,
    "acc": Float,
    "max_combo": Integer,
    "total_hits": Integer,
    "replay_views": Integer,
    "xh_count": Integer,
    "x_count": Integer,
    "sh_count": Integer,
    "s_count": Integer,
    "a_count": Integer,
})

player_model = api.model("Player", {
    "id": Integer,
    "name": String,
    "safe_name": String,
    "priv": Integer,
    "country": String,
    "creation_time": Integer,
    "latest_activity": Integer,
    "preferred_mode": Integer,
    "userpage_content": String,
    "stats": Nested(player_stats_model),
})

leaderboard_model = api.model("Leaderboard", {
    "id": Integer,
    "name": String,
    "pp": Integer,
    "plays": Integer,
    "tscore": Integer,
    "rscore": Integer,
})

beatmap_model = api.model("Beatmap", {
    "id": Integer,
    "set_id": Integer,
    "status": Integer,
    "md5": String,
    "artist": String,
    "title": String,
    "version": String,
    "creator": String,
    "filename": String,
    "last_update": DateTime,
    "total_length": Integer,
    "max_combo": Integer,
    "frozen": Integer,
    "plays": Integer,
    "passes": Integer,
    "mode": Integer,
    "bpm": Float,
    "cs": Float,
    "ar": Float,
    "od": Float,
    "hp": Float,
    "diff": Float,
})

score_model = api.model("Score", {
    "id": Integer,
    "map_md5": String,
    "score": Integer,
    "pp": Float,
    "acc": Float,
    "max_combo": Integer,
    "mods": Integer,
    "n300": Integer,
    "n100": Integer,
    "n50": Integer,
    "nmiss": Integer,
    "ngeki": Integer,
    "nkatu": Integer,
    "grade": String,
    "status": Integer,
    "mode": Integer,
    "play_time": DateTime,
    "time_elapsed": Integer,
    "client_flags": Integer,
    "userid": Integer,
    "perfect": Integer,
    "online_checksum": String,
    "beatmap": Nested(beatmap_model)
})
