import os
from pathlib import Path

import dotenv
import pymysql
from flask import Flask
from flask_jwt_extended import JWTManager
from redis import Redis

dotenv.load_dotenv()


class SkrunglyAPI(Flask):
    def __init__(self, data_dir):
        super().__init__(__name__)

        self._data_dir = Path(data_dir) if data_dir else Path("..") / ".data"
        self._data_dir.mkdir(exist_ok=True)

    def data_path(self, subdir=None):
        if not subdir:
            return self._data_dir

        path = self._data_dir / subdir
        path.mkdir(exist_ok=True)
        return path

    @property
    def osk_dir(self):
        return self.data_path("osk")

    @property
    def skins_dir(self):
        return self.data_path("skins")

    @property
    def banners_dir(self):
        return self.data_path("banners")

    @property
    def assets_dir(self):
        return self.data_path("assets")

    @property
    def font_dir(self):
        return self.data_path("font")


app = SkrunglyAPI(os.environ.get("DATA_FOLDER"))

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
app.config["JWT_SESSION_COOKIE"] = False
app.config["JWT_COOKIE_SECURE"] = True
app.config["PROPAGATE_EXCEPTIONS"] = True

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
