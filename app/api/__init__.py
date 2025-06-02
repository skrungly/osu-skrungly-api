from flask import render_template
from flask_restx import Api, apidoc
from marshmallow import ValidationError

from app import app


@apidoc.apidoc.add_app_template_global
def swagger_static(filename):
    return f"./swaggerui/{filename}"


api = Api(app, version="0.1", title="osu!skrungly API")


@api.errorhandler(ValidationError)
def on_validation_error(err):
    err.data = err.messages
    return {"message": err.data}, 422


@api.documentation
def swagger_docs():
    return render_template(
        "swagger-ui.html",
        title=api.title,
        specs_url="./swagger.json"
    )


from app.api import (  # noqa: F401 E402
    auth, beatmaps, players, scores, stats
)
