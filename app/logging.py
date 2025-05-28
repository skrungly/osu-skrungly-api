import logging

from flask import has_request_context, request
from flask.logging import default_handler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.method = request.method
            record.path = request.path
        return super().format(record)


formatter = RequestFormatter(
    "[%(asctime)s] [%(levelname)s] (%(method)s %(path)s): %(message)s"
)

default_handler.setFormatter(formatter)
