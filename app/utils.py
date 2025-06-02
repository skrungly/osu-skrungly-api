from __future__ import annotations

import os
import re
from enum import IntEnum
from pathlib import Path

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

USERNAME_REGEX = re.compile(r"^[\w \[\]-]+$")


class Mode(IntEnum):
    OSU = 0
    TAIKO = 1
    CATCH = 2
    MANIA = 3

    OSU_RX = 4
    TAIKO_RX = 5
    CATCH_RX = 6
    # MANIA_RX = 7  # not used

    OSU_AP = 8
    # TAIKO_AP = 9  # not used
    # CATCH_AP = 10  # not used
    # MANIA_AP = 11  # not used

    @classmethod
    def from_name_or_id(cls, name_or_id: str) -> Mode:
        if name_or_id.isdigit():
            return Mode(int(name_or_id))

        return Mode[name_or_id.upper().replace("!", "_")]
