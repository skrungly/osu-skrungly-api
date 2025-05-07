import hashlib

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required, set_access_cookies
)

from app import app, db


def authenticate(name=None, password=None):
    if not (name and password):
        return None

    db.ping()
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id, pw_bcrypt FROM users WHERE name = %s", (name,)
        )

        user_info = cursor.fetchone()
        db.commit()

    if not user_info:
        return None

    # the bancho.py service uses a double hash
    pw_md5 = hashlib.md5(password.encode()).hexdigest().encode()
    if not bcrypt.checkpw(pw_md5, user_info["pw_bcrypt"].encode()):
        return None

    return user_info["id"]


@app.route("/auth", methods=["GET", "POST"])
@jwt_required(optional=True)
def auth():
    if request.method == "POST":
        cookie = request.args.get("cookie")
        name = request.args.get("name")
        password = request.args.get("password")

        user_id = authenticate(name, password)
        if user_id is None:
            return {
                "success": False,
                "message": "invalid username or password"
            }, 403

        access_token = create_access_token(identity=str(user_id))
        response_data = {"success": True}

        # two options: if the request wants the JWT as a cookie,
        # then use `set_access_cookies` for CSRF protection with
        # double-submit verification. otherwise, just send the
        # access token in the response.
        if cookie is not None:
            response = jsonify(response_data)
            set_access_cookies(response, access_token)
        else:
            response_data["access_token"] = access_token
            response = jsonify(response_data)

        return response

    elif request.method == "GET":
        return {
            "success": True,
            "logged_in_as": get_jwt_identity(),
        }
