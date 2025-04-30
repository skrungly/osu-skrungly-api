import os

import pymysql
from flask import Flask
from flask_restx import Api

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

api = Api(app)

db = pymysql.connect(
    host=os.environ.get("MYSQL_HOST", "mysql"),
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    db=os.environ["MYSQL_DATABASE"],
    cursorclass=pymysql.cursors.DictCursor,
)

from app import routes  # noqa: F401 E402
