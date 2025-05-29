from flask import abort
from flask_restx import Api, reqparse
from werkzeug.datastructures import FileStorage

from app import app

api = Api(app)

upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'file', location='files', type=FileStorage, required=True
)


class PaginatedRequestParser(reqparse.RequestParser):
    def __init__(self, *args, max_limit=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_limit = max_limit

        self.add_argument("page", type=int, default=0)
        self.add_argument("limit", type=int, default=10)

    def parse_args(self, *args, **kwargs):
        req_args = super().parse_args(*args, **kwargs)

        if req_args["limit"] > self.max_limit:
            abort(422)

        return req_args


from app.api import (  # noqa: F401 E402
    auth, beatmaps, players, scores, stats
)
