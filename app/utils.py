import os
import re
from pathlib import Path

from app import db

DATA_DIR = Path("..") / os.environ.get("DATA_FOLDER", ".data")
DATA_DIR.mkdir(exist_ok=True)

OSK_DIR = DATA_DIR / "osk"
OSK_DIR.mkdir(exist_ok=True)

SKINS_DIR = DATA_DIR / "skins"
SKINS_DIR.mkdir(exist_ok=True)

DEFAULT_SKIN_URL = os.environ.get("DEFAULT_SKIN_URL")
DEFAULT_SKIN_ID = "default"

BANNERS_DIR = DATA_DIR / "banners"
BANNERS_DIR.mkdir(exist_ok=True)

ASSETS_DIR = DATA_DIR / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

FONT_DIR = ASSETS_DIR / "font"
FONT_DIR.mkdir(exist_ok=True)
FONT_URL = os.environ.get("FONT_URL")

MAX_SKIN_SIZE = int(os.environ.get("SKIN_MAX_SIZE") or 256 * 1024 * 1024)

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


def resolve_mode_id(id_or_name: str):
    if id_or_name.isdigit():
        return id_or_name

    return MODE_NAMES.get(id_or_name)
