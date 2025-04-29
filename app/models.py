from flask_restx.fields import Float, Integer, String

from app import api

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

leaderboard_model = api.model("Leaderboard", {
    "id": Integer,
    "name": String,
    "pp": Integer,
    "plays": Integer,
    "tscore": Integer,
    "rscore": Integer,
})
