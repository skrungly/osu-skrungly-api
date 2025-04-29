import os

import pymysql
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

db = pymysql.connect(
    host=os.environ.get("MYSQL_HOST", "mysql"),
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    db=os.environ["MYSQL_DATABASE"],
    cursorclass=pymysql.cursors.DictCursor,
)

from app.resources import PlayerAPI, PlayerListAPI  # noqa: E402

api.add_resource(PlayerAPI, "/players/<int:user_id>", endpoint="player")
api.add_resource(PlayerListAPI, "/players", endpoint="players")
