import os

import dotenv
import pymysql
from flask import Flask
from flask_restx import Api

dotenv.load_dotenv()

app = Flask(__name__)
api = Api(app)

db = pymysql.connect(
    host=os.environ["MYSQL_HOST"],
    port=int(os.environ["MYSQL_PORT"]),
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    db=os.environ["MYSQL_DATABASE"],
    cursorclass=pymysql.cursors.DictCursor,
)

from app import routes  # noqa: F401 E402
