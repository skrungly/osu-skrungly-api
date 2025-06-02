import os

import dotenv
import pymysql
from flask import Flask
from flask_jwt_extended import JWTManager
from redis import Redis

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
app.config["JWT_SESSION_COOKIE"] = False
app.config["JWT_COOKIE_SECURE"] = True

jwt = JWTManager(app)

redis = Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    username=os.environ.get("REDIS_USERNAME", "default"),
    password=os.environ.get("REDIS_PASSWORD"),
    db=0,
    decode_responses=True,
)

db = pymysql.connect(
    host=os.environ["MYSQL_HOST"],
    port=int(os.environ["MYSQL_PORT"]),
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    db=os.environ["MYSQL_DATABASE"],
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True,
)

from app import logging, replay, skins, utils  # noqa: F401 E402
from app.api import api  # noqa: F401 E402
