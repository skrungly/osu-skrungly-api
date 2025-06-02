import hashlib

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from flask_restx import Resource

from app import app, db, jwt, models, redis
from app.api import api

REFRESH_TOKEN_CLAIM = "refresh"

namespace = api.namespace(
    name="auth",
    description="manage authentication and tokens",
)


def authenticate(name=None, password=None):
    if not (name and password):
        return None

    db.ping()
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id, pw_bcrypt FROM users WHERE name = %s", (name,)
        )

        user_info = cursor.fetchone()

    if not user_info:
        return None

    # the bancho.py service uses a double hash
    pw_md5 = hashlib.md5(password.encode()).hexdigest().encode()
    if not bcrypt.checkpw(pw_md5, user_info["pw_bcrypt"].encode()):
        return None

    return str(user_info["id"])


def create_tokens(identity, refresh_token=None):
    if refresh_token is None:
        refresh_token = create_refresh_token(identity=identity)
        namespace.logger.debug(f"created refresh token for user {identity}")

    access_token = create_access_token(
        identity=identity,
        additional_claims={REFRESH_TOKEN_CLAIM: refresh_token}
    )

    namespace.logger.debug(f"created access token for user {identity}")
    return access_token, refresh_token


@jwt.token_in_blocklist_loader
def check_token_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return redis.get(jti) is not None


@namespace.route("/identity")
class Identity(Resource):
    @jwt_required(optional=True)
    def get(self):
        return jsonify(identity=get_jwt_identity())


@namespace.route("/login")
class Login(Resource):
    def post(self):
        login_args = models.LoginOptionsSchema().load(request.get_json())

        user_id = authenticate(login_args["name"], login_args["password"])
        if user_id is None:
            return {"message": "invalid username or password"}, 401

        access_token, refresh_token = create_tokens(user_id)

        # two options: if the request wants the JWT as a cookie,
        # then use `set_access_cookies` for CSRF protection with
        # double-submit verification. otherwise, just send the
        # access token in the response.
        if login_args["cookie"]:
            response = jsonify(identity=user_id)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

        return jsonify(
            identity=user_id,
            access_token=access_token,
            refresh_token=refresh_token
        )


@namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        using_cookies = False
        refresh_token = None

        # grab the refresh token from the current response headers so that
        # it can be inserted into the new access token claims. first try
        # scanning the "Authorization" header (or whatever is configured)
        auth_bearer = request.headers.environ.get(
            f"HTTP_{app.config["JWT_HEADER_NAME"].upper()}"
        )

        if auth_bearer is not None:
            # extract the token from the "Bearer <Token>" formatting
            refresh_token = auth_bearer.replace(
                app.config["JWT_HEADER_TYPE"], ""
            ).strip()

        else:
            using_cookies = True
            refresh_token = request.cookies.get(
                app.config["JWT_REFRESH_COOKIE_NAME"]
            )

        # we should definitely have a `refresh_token` value now, but it
        # would feel wrong to skip this check:
        if refresh_token is None:
            return {"message": "unable to find refresh token"}, 401

        access_token, _ = create_tokens(identity, refresh_token)

        if using_cookies:
            response = jsonify(identity=identity)
            set_access_cookies(response, access_token)
            return response

        return jsonify(identity=identity, access_token=access_token)


@namespace.route("/logout")
class Logout(Resource):
    @jwt_required()
    def delete(self):
        token = get_jwt()
        identity = get_jwt_identity()
        redis.set(token["jti"], "", ex=app.config["JWT_ACCESS_TOKEN_EXPIRES"])

        refresh_token = token.get(REFRESH_TOKEN_CLAIM)
        refresh_jti = get_jti(refresh_token)
        redis.set(refresh_jti, "", ex=app.config["JWT_REFRESH_TOKEN_EXPIRES"])

        response = jsonify(identity=None)
        unset_jwt_cookies(response)

        namespace.logger.debug(f"revoked a refresh token for user {identity}")
        return response
