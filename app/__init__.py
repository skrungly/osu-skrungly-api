import os

import dotenv
import pymysql
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api
from redis import Redis

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"

jwt = JWTManager(app)
api = Api(app)

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
)

from app import auth, routes  # noqa: F401 E402
