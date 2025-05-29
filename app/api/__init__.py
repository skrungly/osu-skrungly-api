from flask_restx import Api

from app import app

api = Api(app)

from app.api import (  # noqa: F401 E402
    auth, beatmaps, players, scores, stats
)
