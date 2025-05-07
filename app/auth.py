import hashlib

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
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


@app.route("/auth", methods=["GET"])
@jwt_required(optional=True)
def auth_check():
    return {
        "success": True,
        "logged_in_as": get_jwt_identity(),
    }


@app.route("/auth/login", methods=["POST"])
def auth_login():
    name = request.args.get("name")
    password = request.args.get("password")

    user_id = authenticate(name, password)
    if user_id is None:
        return jsonify(
            success=False,
            message="invalid username or password"
        ), 403

    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))

    # two options: if the request wants the JWT as a cookie,
    # then use `set_access_cookies` for CSRF protection with
    # double-submit verification. otherwise, just send the
    # access token in the response.
    if "cookie" in request.args:
        response = jsonify(success=True)
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response

    return jsonify(
        success=True,
        access_token=access_token,
        refresh_token=refresh_token,
    )


@app.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def auth_refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    if "cookie" in request.args:
        response = jsonify(success=True)
        set_access_cookies(response, access_token)
        return response

    return jsonify(success=True, access_token=access_token)
