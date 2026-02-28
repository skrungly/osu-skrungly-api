from __future__ import annotations

import os
import re
from enum import IntEnum
from io import BytesIO

import requests

DEFAULT_SKIN_URL = os.environ.get("DEFAULT_SKIN_URL")
DEFAULT_SKIN_ID = "default"
MAX_SKIN_SIZE = int(os.environ.get("SKIN_MAX_SIZE") or 256 * 1024 * 1024)

BEATMAP_BG_MIRRORS = os.environ["BEATMAP_BG_MIRRORS"].split(",")
BEATMAP_OSZ_MIRRORS = os.environ["BEATMAP_OSZ_MIRRORS"].split(",")
MAX_OSZ_SIZE = int(os.environ.get("OSZ_MAX_SIZE") or 64 * 1024 * 1024)

FONT_URL = os.environ.get("FONT_URL")

USERNAME_REGEX = re.compile(r"^[\w \[\]-]+$")


def fetch_beatmap_osz(set_id):
    for api_url in BEATMAP_OSZ_MIRRORS:
        osz_url = api_url.format(set_id=set_id)

        response = requests.get(osz_url, stream=True)
        if response.status_code != 200:
            continue

        content_length = int(response.headers["Content-Length"])
        if content_length > MAX_OSZ_SIZE:
            raise RuntimeError("beatmap download exceeds maximum size")

        size = 0
        osz_data = b""
        for chunk in response.iter_content(1024 * 1024):
            size += len(chunk)

            if size > MAX_OSZ_SIZE:
                raise RuntimeError("beatmap download exceeds maximum size")

            osz_data += chunk

        return BytesIO(osz_data)


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
