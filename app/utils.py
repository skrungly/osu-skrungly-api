import re

from flask import abort
from flask_restx import reqparse

from app import db

MODE_NAMES = {
    "osu": 0,
    "taiko": 1,
    "catch": 2,
    "mania": 3,
    "relax": 4,
}

USERNAME_REGEX = re.compile(r"^[\w \[\]-]{2,15}$")


# name and password validation logic is copied from bancho.py
# TODO: create an endpoint on bancho for checking these things,
# so that this logic is not repeated across services!
def valid_username(name):
    if not USERNAME_REGEX.match(name):
        return False

    if "_" in name and " " in name:
        return False

    db.ping()
    with db.cursor() as cursor:
        cursor.execute("SELECT name FROM users WHERE name = %s", (name,))
        existing_entry = cursor.fetchone()
        db.commit()

    if existing_entry:
        return False

    return True


def valid_password(password):
    if not 8 <= len(password) <= 32:
        return False

    if len(set(password)) <= 3:
        return False

    return True


def resolve_player_id(id_or_name: str):
    if id_or_name.isdigit():
        return id_or_name

    db.ping()
    with db.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE name = %s", (id_or_name,))
        player_id = cursor.fetchone()
        db.commit()

    if player_id is not None:
        return player_id["id"]


def resolve_mode_id(id_or_name: str):
    if id_or_name.isdigit():
        return id_or_name

    return MODE_NAMES.get(id_or_name)


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
