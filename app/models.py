from marshmallow import Schema, fields


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
    id = fields.Int(dump_only=True)
    name = fields.Str()
    password = fields.Str(load_only=True)
    safe_name = fields.Str(dump_only=True)
    priv = fields.Int(dump_only=True)
    country = fields.Str(dump_only=True)
    creation_time = fields.Int(dump_only=True)
    latest_activity = fields.Int(dump_only=True)
    preferred_mode = fields.Int()
    userpage_content = fields.Str()
    stats = fields.List(
        fields.Nested(PlayerStatsSchema),
        dump_only=True
    )


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
    beatmap = fields.Nested(BeatmapSchema)


# schemas for deserialising options:
class FileUploadSchema(Schema):
    file = fields.Raw(
        metadata={'type': 'string', 'format': 'binary'},
        required=True,
    )


class LoginOptionsSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)
    cookie = fields.Bool(load_default=False)


class PageOptionsSchema(Schema):
    page = fields.Int(load_default=0)
    limit = fields.Int(load_default=10)


# TODO: `mode` should probably be its own type of field
class PlayerStatsOptionsSchema(Schema):
    mode = fields.Str(required=True)


class PlayerListOptionsSchema(PageOptionsSchema):
    sort = fields.Str(load_default="pp")
    mode = fields.Str(required=True)


class PlayerScoresOptionsSchema(PageOptionsSchema):
    sort = fields.Str(load_default="pp")
    mode = fields.Str()
