from marshmallow import Schema, fields, validate, validates, ValidationError

from app import db
from app.utils import Mode, USERNAME_REGEX


class ModeField(fields.Field[Mode]):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(value)

    def _deserialize(self, value, attr, obj, **kwargs):
        try:
            return Mode.from_name_or_id(value)

        except ValueError as error:
            modes = tuple(int(m) for m in Mode)
            raise ValidationError(f"id must be one of {modes}") from error

        except KeyError as error:
            modes = tuple(m.name.replace("_", "!").lower() for m in Mode)
            raise ValidationError(f"name must be one of {modes}") from error


# schemas for serialising data:
class GlobalStatsSchema(Schema):
    tscore = fields.Int()
    rscore = fields.Int()
    pp = fields.Int()
    plays = fields.Int()
    playtime = fields.Int()
    total_hits = fields.Int()


class PlayerStatsSchema(Schema):
    id = fields.Int()
    mode = fields.Int()
    tscore = fields.Int()
    rscore = fields.Int()
    pp = fields.Int()
    plays = fields.Int()
    playtime = fields.Int()
    acc = fields.Float()
    max_combo = fields.Int()
    total_hits = fields.Int()
    replay_views = fields.Int()
    xh_count = fields.Int()
    x_count = fields.Int()
    sh_count = fields.Int()
    s_count = fields.Int()
    a_count = fields.Int()


# TODO: move validation logic to these schemas
class PlayerSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    password = fields.Str()
    safe_name = fields.Str()
    priv = fields.Int()
    country = fields.Str()
    creation_time = fields.Int()
    latest_activity = fields.Int()
    preferred_mode = fields.Int()
    userpage_content = fields.Str()
    stats = fields.List(fields.Nested(PlayerStatsSchema))


# TODO: maybe borrow fields from PlayerSchema and/or GlobalStatsSchema
class LeaderboardSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    pp = fields.Int()
    plays = fields.Int()
    tscore = fields.Int()
    rscore = fields.Int()


class BeatmapSchema(Schema):
    id = fields.Int()
    set_id = fields.Int()
    status = fields.Int()
    md5 = fields.Str()
    artist = fields.Str()
    title = fields.Str()
    version = fields.Str()
    creator = fields.Str()
    filename = fields.Str()
    last_update = fields.DateTime()
    total_length = fields.Int()
    max_combo = fields.Int()
    frozen = fields.Int()
    plays = fields.Int()
    passes = fields.Int()
    mode = fields.Int()
    bpm = fields.Float()
    cs = fields.Float()
    ar = fields.Float()
    od = fields.Float()
    hp = fields.Float()
    diff = fields.Float()

    # custom property, given when sorting by popularity
    popularity = fields.Int()


class ScoreSchema(Schema):
    id = fields.Int()
    map_md5 = fields.Str()
    score = fields.Int()
    pp = fields.Float()
    acc = fields.Float()
    max_combo = fields.Int()
    mods = fields.Int()
    n300 = fields.Int()
    n100 = fields.Int()
    n50 = fields.Int()
    nmiss = fields.Int()
    ngeki = fields.Int()
    nkatu = fields.Int()
    grade = fields.Str()
    status = fields.Int()
    mode = fields.Int()
    play_time = fields.DateTime()
    time_elapsed = fields.Int()
    client_flags = fields.Int()
    userid = fields.Int()
    perfect = fields.Int()
    online_checksum = fields.Str()

    # nested data
    beatmap = fields.Nested(BeatmapSchema)
    player = fields.Nested(PlayerSchema)


# schemas for deserialising and validating options:
class FileUploadSchema(Schema):
    file = fields.Raw(
        metadata={'type': 'string', 'format': 'binary'},
        required=True,
    )


class LoginOptionsSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)
    cookie = fields.Bool(load_default=False)


class PlayerEditOptionsSchema(Schema):
    name = fields.Str()
    password = fields.Str()
    userpage_content = fields.Str()
    preferred_mode = ModeField()

    # name and password validation logic is copied from bancho.py
    # TODO: maybe create an endpoint on bancho for validation checks?
    @validates("name")
    def validate_name(self, value: str, data_key: str) -> None:
        errors = []

        if not 2 <= len(value) <= 15:
            errors.append("must be 2-15 characters in length")

        if not USERNAME_REGEX.match(value):
            errors.append("contains invalid characters")

        if "_" in value and " " in value:
            errors.append("may contain ' ' or '_' but not both")

        db.ping()
        with db.cursor() as cursor:
            cursor.execute("SELECT name FROM users WHERE name = %s", (value,))
            existing_entry = cursor.fetchone()

        if existing_entry:
            errors.append("already taken by another player")

        if errors:
            raise ValidationError(errors)

    @validates("password")
    def validate_password(self, value: str, data_key: str) -> None:
        errors = []

        if not 8 <= len(value) <= 32:
            errors.append("must be 8-32 characters in length")

        if len(set(value)) <= 3:
            errors.append("must contain at least 3 unique characters")

        if errors:
            raise ValidationError(errors)

    @validates("userpage_content")
    def validates_userpage_content(self, value: str, data_key: str) -> None:
        if len(value) > 2048:
            raise ValidationError("must be no longer than 2048 characters")


class PageOptionsSchema(Schema):
    page = fields.Int(load_default=0)
    limit = fields.Int(load_default=10)


class PlayerStatsOptionsSchema(Schema):
    mode = ModeField(required=True)


class PlayerListOptionsSchema(PageOptionsSchema):
    sort = fields.Str(load_default="pp")
    online = fields.Bool(load_default=False)
    mode = ModeField(required=True)


class PlayerScoresOptionsSchema(PageOptionsSchema):
    sort = fields.Str(load_default="pp")
    mode = ModeField()


class ScoresOptionsSchema(PageOptionsSchema):
    _SORT_OPTIONS = {
        "recent": "id",
        "score": "score",
        "pp": "pp",
        "combo": "max_combo",
        "length": "time_elapsed",
    }

    _STATUS_ALIASES = {
        "0": {0},  # bit lazy but it's easier to work with
        "1": {1},
        "2": {2},
        "failed": {0},
        "passed": {1, 2},
        "best": {2},
        "all": {0, 1, 2},
    }

    sort = fields.Str(
        validate=validate.OneOf(_SORT_OPTIONS),
        load_default="recent"
    )
    mods = fields.Int()
    grade = fields.Str()
    mode = ModeField()
    status = fields.Str(
        validate=validate.OneOf(_STATUS_ALIASES),
        load_default="passed"
    )
    beatmap = fields.Str()
    player = fields.Str()

    @validates("beatmap")
    def validates_beatmap(self, value: str, data_key: str) -> None:
        if value.isdigit():
            return

        # length and hexadecimal check for md5 sums
        if len(value) == 32 and not set(value) - set("abcdef0123456789"):
            return

        raise ValidationError("invalid beatmap id or md5")


class BeatmapsOptionsSchema(PageOptionsSchema):
    _SORT_OPTIONS = {
        "plays": "plays",
        "passes": "passes",
        "diff": "diff",
        "length": "total_length",
        "popular": None,  # more involved than just a db key
    }

    _STATUS_ALIASES = {
        "0": {0},
        "2": {2},
        "3": {3},
        "4": {4},
        "5": {5},
        "pending": {0},
        "ranked": {2},
        "approved": {3},
        "qualified": {4},
        "loved": {5},
        "leaderboard": {2, 3, 4, 5},
        "all": {0, 2, 3, 4, 5}
    }

    sort = fields.Str(
        validate=validate.OneOf(_SORT_OPTIONS),
        load_default="passes",
    )
    status = fields.Str(validate=validate.OneOf(_STATUS_ALIASES))
    mode = ModeField()
    set_id = fields.Int()
    frozen = fields.Bool()
