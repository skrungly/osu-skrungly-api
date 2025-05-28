from flask_restx import Api

from app import app

api = Api(app)

from app.api import auth  # noqa: F401 E402
