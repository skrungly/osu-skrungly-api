"""
programmatically generate screenshots of osu! replays.

this code has been hastily cut-and-pasted from the discord bot and is
therefore about as bulletproof as a sheet of paper. nonetheless, it gets
the job done and (with some work) may be worth releasing as a package.
"""

from enum import IntFlag
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

from app.utils import DEFAULT_SKIN_ID, FONT_DIR, FONT_URL, SKINS_DIR

REPLAY_WIDTH = 1920
REPLAY_HEIGHT = 1080
REPLAY_ASPECT = REPLAY_WIDTH / REPLAY_HEIGHT
REPLAY_RESOLUTION = (REPLAY_WIDTH, REPLAY_HEIGHT)

BG_IMAGE_URLS = [  # TODO: might be time to make a custom mirror?
    "https://beatconnect.io/bg/{set_id}/{id}",
    "https://b.ppy.sh/thumb/{set_id}l.jpg",
]

DEFAULT_SKIN_DIR = SKINS_DIR / DEFAULT_SKIN_ID

# the top 1/8th of the screen is a dark header for map info
HEADER_HEIGHT = REPLAY_HEIGHT // 8 - 1

TITLE_FONT_SIZE = REPLAY_HEIGHT / 26
SMALL_FONT_SIZE = REPLAY_HEIGHT / 36

FONT_VSPACE = REPLAY_HEIGHT // 360
FONT_HSPACE = REPLAY_WIDTH // 240

NUMERIC_CHARS = (
    *((char, char) for char in "0123456789x"),
    ("dot", "."),
    ("comma", ","),
    ("percent", "%")
)

SCORE_SCALE = REPLAY_HEIGHT / 1175  # ish?
HIT_SCALE = REPLAY_HEIGHT / 1375  # also ish?

SCORE_X = 8 + REPLAY_HEIGHT // 4
SCORE_Y = (REPLAY_HEIGHT * 7) // 36
SCORE_SPACING = REPLAY_HEIGHT // 180

HIT_OFFSET_X = REPLAY_HEIGHT // 12
HIT_OFFSET_Y = -REPLAY_HEIGHT // 24 + 10
HIT_SPACING = 0

# the panel starts at a 1/120th gap below the 1/8th header
PANEL_START = (REPLAY_HEIGHT * 2) // 15
PANEL_SCALE = REPLAY_HEIGHT / 1536  # 768 @ 1x

JUDGE_COLS = [int(REPLAY_HEIGHT * x) for x in (1/12, 1/2)]
JUDGE_ROWS = [int(REPLAY_HEIGHT * y) for y in (1/3, 1/3 + 1/8, 1/3 + 2/8)]

# table positions, db keys, and skin elements, for each gamemode
JUDGE_NAMES = [
    [  # osu!standard:
        ("n300", "hit300"), ("ngeki", "hit300g"),
        ("n100", "hit100"), ("nkatu", "hit100k"),
        ("n50", "hit50"), ("nmiss", "hit0")
    ],
    [  # osu!taiko:
        ("n300", "taiko-hit300"), ("ngeki", "taiko-hit300g"),
        ("n100", "taiko-hit100"), ("nkatu", "taiko-hit100k"),
        ("nmiss", "taiko-hit0"), (None, None)
    ],
    [  # osu!catch: (could be made better!)
        ("n300", "fruit-orange"), ("nmiss", "hit0"),
        ("n100", "fruit-drop"), (None, None),
        ("n50", "fruit-drop"), (None, None)
    ],
    [  # osu!mania
        ("n300", "mania-hit300"), ("ngeki", "mania-hit300g-0"),
        ("nkatu", "mania-hit200"), ("n100", "mania-hit100"),
        ("n50", "mania-hit50"), ("nmiss", "mania-hit0")
    ]
]

JUDGE_SCALE = REPLAY_HEIGHT / 3072

GRADE_X = REPLAY_WIDTH - REPLAY_HEIGHT // 4
GRADE_Y = REPLAY_HEIGHT // 2.4
GRADE_SCALE = REPLAY_HEIGHT / 1536

MODS_X = REPLAY_WIDTH - REPLAY_HEIGHT // 12
MODS_Y = (REPLAY_HEIGHT * 49) // 90
MODS_SPACING = REPLAY_HEIGHT // 24
MODS_SCALE = REPLAY_HEIGHT / 1532

GRAPH_X = REPLAY_HEIGHT // 3
GRAPH_Y = (REPLAY_HEIGHT * 19) // 24
GRAPH_SCALE = REPLAY_HEIGHT / 1532

PERF_X = (REPLAY_HEIGHT * 13) // 24
PERF_Y = (REPLAY_HEIGHT * 43) // 48
PERF_SCALE = REPLAY_HEIGHT / 1532

TITLE_X_RIGHT = (REPLAY_WIDTH * 125) // 128
TITLE_Y = 0
TITLE_SCALE = REPLAY_HEIGHT / 1532

ACC_X = int(REPLAY_HEIGHT // 2.64)
COMBO_X = int(REPLAY_HEIGHT // 96)

STATS_Y = int(REPLAY_HEIGHT // 1.6)
STATS_SCALE = REPLAY_HEIGHT / 1532
STATS_OFFSET_X = REPLAY_HEIGHT // 50
STATS_OFFSET_Y = REPLAY_HEIGHT // 16


class Mods(IntFlag):
    NOFAIL = "NF"
    EASY = "EZ"
    TOUCH_SCREEN = "TS"
    HIDDEN = "HD"
    HARDROCK = "HR"
    SUDDENDEATH = "SD"
    DOUBLETIME = "DT"
    RELAX = "RX"
    HALFTIME = "HT"
    NIGHTCORE = "NC"
    FLASHLIGHT = "FL"
    AUTOPLAY = "AT"
    SPUNOUT = "SO"
    RELAX2 = "AP"
    PERFECT = "PF"
    KEY4 = "4K"
    KEY5 = "5K"
    KEY6 = "6K"
    KEY7 = "7K"
    KEY8 = "8K"
    FADEIN = "FI"
    RANDOM = "RD"
    CINEMA = "CM"
    TARGET = "TP"
    KEY9 = "9K"
    KEYCOOP = "CP"
    KEY1 = "1K"
    KEY3 = "3K"
    KEY2 = "2K"
    SCOREV2 = "V2"
    MIRROR = "MR"

    def __new__(cls, acronym):
        # a little bit jank but... it's fiiiiine.
        value = 1 << len(cls._member_names_)
        member = int.__new__(cls, value)
        member._value_ = value
        member.acronym = acronym
        return member

    @property
    def skin_name(self):
        if len(self) != 1:
            raise ValueError("expected single mod for skin element")

        return f"selection-mod-{self.name.lower()}"


def _scale_image(img, scale):
    new_width = max(1, int(img.width * scale))
    new_height = max(1, int(img.height * scale))
    return img.resize((new_width, new_height))


def _skin_element(name, skin):
    for skin_path in (SKINS_DIR / skin, DEFAULT_SKIN_DIR):
        try:
            return Image.open(skin_path / f"{name}@2x.png").convert("RGBA")
        except (FileNotFoundError, UnidentifiedImageError):
            pass

        try:
            small = Image.open(skin_path / f"{name}.png").convert("RGBA")
            return _scale_image(small, 2)
        except (FileNotFoundError, UnidentifiedImageError):
            pass

    return Image.new("RGBA", (1, 1), (0, 0, 0, 0))


def _paste_centred_scaled(bg, fg, x, y, scale):
    resized = _scale_image(fg, scale)

    adjusted_x = int(x - resized.width // 2)
    adjusted_y = int(y - resized.height // 2)

    bg.paste(resized, (adjusted_x, adjusted_y), resized)


def _write_score_text(img, text, x, y, charset, spacing=0):
    char_pos = x
    for char in text:
        char_img = charset[char]
        img.paste(char_img, (char_pos, y), char_img)
        char_pos += char_img.width + spacing


def _fetch_bg_image(beatmap):
    for api_url in BG_IMAGE_URLS:
        bg_url = api_url.format(**beatmap)
        response = requests.get(bg_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))

    # if no source was found, fallback to plain black
    return Image.new("RGBA", REPLAY_RESOLUTION)


def get_font_path(*, download=False):
    for font_path in FONT_DIR.iterdir():
        return font_path

    if not download or not FONT_URL:
        return None

    response = requests.get(FONT_URL)
    font_path = FONT_DIR / Path(FONT_URL).name
    with open(font_path, "wb") as font:
        font.write(response.content)

    return font_path


def get_replay_screen(score, beatmap, username, skin):
    font_path = get_font_path()
    title_font = ImageFont.truetype(str(font_path), TITLE_FONT_SIZE)
    small_font = ImageFont.truetype(str(font_path), SMALL_FONT_SIZE)

    source_bg = _fetch_bg_image(beatmap)
    source_aspect = source_bg.width / source_bg.height

    crop_left = 0
    crop_top = 0
    crop_right = source_bg.width
    crop_bottom = source_bg.height

    # crop to the required aspect ratio
    if source_aspect > REPLAY_ASPECT:
        new_width = source_bg.height * REPLAY_ASPECT
        crop_left = (source_bg.width - new_width) // 2
        crop_right = crop_left + new_width
    else:
        new_height = source_bg.width / REPLAY_ASPECT
        crop_top = (source_bg.height - new_height) // 2
        crop_bottom = crop_top + new_height

    crop_box = (crop_left, crop_top, crop_right, crop_bottom)
    replay_img = source_bg.crop(crop_box).resize(REPLAY_RESOLUTION)
    draw = ImageDraw.Draw(replay_img, "RGBA")

    # the background of the map is darkened by 40%
    draw.rectangle((0, 0, *REPLAY_RESOLUTION), fill=(0, 0, 0, 102))

    # then draw a shaded rectangle for the header text
    draw.rectangle((0, 0, REPLAY_WIDTH, HEADER_HEIGHT), fill=(0, 0, 0, 204))

    draw.text(
        (FONT_HSPACE, 0),
        f"{beatmap['artist']} - {beatmap['title']} [{beatmap['version']}]",
        font=title_font
    )

    draw.text(
        (FONT_HSPACE, TITLE_FONT_SIZE + FONT_VSPACE),
        f"Beatmap by {beatmap['creator']}",
        font=small_font
    )

    draw.text(
        (FONT_HSPACE, TITLE_FONT_SIZE + SMALL_FONT_SIZE + FONT_VSPACE * 2),
        f"Played by {username} on {score['play_time']:%d/%m/%Y %H:%M:%S}.",
        font=small_font
    )

    # start putting together all of the skin elements
    SCORE_CHARSET = {}
    HIT_CHARSET = {}
    for name, char in NUMERIC_CHARS:
        char_img = _skin_element(f"score-{name}", skin)
        SCORE_CHARSET[char] = _scale_image(char_img, SCORE_SCALE)
        HIT_CHARSET[char] = _scale_image(char_img, HIT_SCALE)

    with _skin_element("ranking-panel", skin) as panel_img:
        panel_img = _scale_image(panel_img, PANEL_SCALE)
        replay_img.paste(panel_img, (0, PANEL_START), panel_img)

    # this is roughly how the game seems to scale the judgements
    for index, (db_key, name) in enumerate(JUDGE_NAMES[score['mode'] % 4]):
        if not db_key:
            continue

        judge_col = index % 2
        judge_row = index // 2
        x = JUDGE_COLS[judge_col]
        y = JUDGE_ROWS[judge_row]

        with _skin_element(name, skin) as judge_img:
            _paste_centred_scaled(replay_img, judge_img, x, y, JUDGE_SCALE)
            _write_score_text(
                replay_img,
                f"{score[db_key]}x",
                x + HIT_OFFSET_X,
                y + HIT_OFFSET_Y,
                HIT_CHARSET,
                HIT_SPACING
            )

    with _skin_element(f"ranking-{score['grade']}", skin) as grade_img:
        _paste_centred_scaled(
            replay_img,
            grade_img,
            GRADE_X,
            GRADE_Y,
            GRADE_SCALE
        )

    with _skin_element("ranking-graph", skin) as graph_img:
        graph_img = _scale_image(graph_img, GRAPH_SCALE)
        replay_img.paste(graph_img, (GRAPH_X, GRAPH_Y), graph_img)

    if score["perfect"]:
        with _skin_element("ranking-perfect", skin) as perf_img:
            _paste_centred_scaled(
                replay_img,
                perf_img,
                PERF_X,
                PERF_Y,
                PERF_SCALE
            )

    with _skin_element("ranking-title", skin) as title_img:
        title_img = _scale_image(title_img, TITLE_SCALE)
        replay_img.paste(
            title_img,
            (TITLE_X_RIGHT - title_img.width, TITLE_Y),
            title_img
        )

    _write_score_text(
        replay_img,
        f"{score['score']:07}",
        SCORE_X,
        SCORE_Y - SCORE_CHARSET["0"].height // 2,
        SCORE_CHARSET,
        SCORE_SPACING
    )

    with _skin_element("ranking-accuracy", skin) as acc_img:
        acc_img = _scale_image(acc_img, STATS_SCALE)
        replay_img.paste(acc_img, (ACC_X, STATS_Y), acc_img)

    _write_score_text(
        replay_img,
        f"{score['acc']:.02f}%",
        ACC_X + STATS_OFFSET_X,
        STATS_Y + STATS_OFFSET_Y,
        HIT_CHARSET,
        HIT_SPACING
    )

    with _skin_element("ranking-maxcombo", skin) as combo_img:
        combo_img = _scale_image(combo_img, STATS_SCALE)
        replay_img.paste(combo_img, (COMBO_X, STATS_Y), combo_img)

    _write_score_text(
        replay_img,
        f"{score['max_combo']}x",
        COMBO_X + STATS_OFFSET_X,
        STATS_Y + STATS_OFFSET_Y,
        HIT_CHARSET,
        HIT_SPACING
    )

    for index, mod in enumerate(Mods(score["mods"])):
        with _skin_element(mod.skin_name, skin) as mod_img:
            _paste_centred_scaled(
                replay_img,
                mod_img,
                MODS_X - MODS_SPACING * index,
                MODS_Y,
                MODS_SCALE
            )

    return replay_img
