import pytest

# (sort by ...) => <target>
SORT_OPTIONS = {
    "recent": "id",  # default
    "score": "score",
    "pp": "pp",
    "combo": "max_combo",
    "length": "time_elapsed",
}

# (filter by ...) => {<source>: <attribute>}
BASIC_FILTER_OPTIONS = {
    "mods": {"score": "mods"},
    "grade": {"score": "grade"},

    # beatmaps and players may each be filtered in two different ways
    "beatmap": {
        "score": "map_md5",
        "beatmap": "id",
    },

    "player": {
        "score": "userid",
        "player": "name",
    },
}

# (status alias) => (expected status values)
STATUS_ALIASES = {
    "failed": {0},
    "passed": {1, 2},  # default
    "best": {2},
    "all": {0, 1, 2},
}


@pytest.mark.parametrize("sort_by", (None, *SORT_OPTIONS))
def test_get_scores_sorted(client, sort_by):
    params = None if sort_by is None else {"sort": sort_by}

    response = client.get("/scores", query_string=params)

    assert response.status_code == 200
    assert len(response.json) > 0

    # now make sure the result is sorted correctly
    previous_value = None
    db_column = SORT_OPTIONS[sort_by or "recent"]
    for score in response.json:
        if previous_value is not None:
            assert previous_value > score[db_column]

        previous_value = score[db_column]

        # sorting by pp should only return ranked/approved scores
        if sort_by == "pp":
            assert response.json["beatmap"]["status"] in (2, 3)


@pytest.mark.parametrize("filter_by", BASIC_FILTER_OPTIONS)
def test_get_scores_filtered_basic(client, expected_data, filter_by):
    filter_options = BASIC_FILTER_OPTIONS[filter_by]
    matching_value = filter_options["score"]
    expected_score = expected_data("score")

    for source, key in filter_options.items():
        value = expected_data(source)[key]

        response = client.get(
            "/scores",
            query_string={
                filter_by: value,
                "limit": 100,  # TODO: put max limit in app.config
            }
        )

        assert response.status_code == 200
        assert len(response.json) > 0

        expected_score_visited = False
        for score in response.json:
            if score["id"] == expected_score["id"]:
                expected_score_visited = True

            assert score[matching_value] == expected_score[matching_value]

        assert expected_score_visited


@pytest.mark.parametrize("status", (None, 0, 1, 2, *STATUS_ALIASES))
def test_get_scores_filtered_by_status(client, status):
    params = None if status is None else {"status": status}

    response = client.get("/scores", query_string=params)

    assert response.status_code == 200
    assert len(response.json) > 0

    # now figure out expected values
    if status is None:
        status = "passed"

    expected_statuses = STATUS_ALIASES.get(status) or {status}

    for score in response.json:
        assert score["status"] in expected_statuses


def test_get_scores_with_compound_query(client, expected_data):
    expected_score = expected_data("score")
    expected_beatmap = expected_data("beatmap")
    expected_player = expected_data("player")

    # collect some filters that still match the expected score
    params = {"limit": 100}
    for filter_by, attributes in BASIC_FILTER_OPTIONS.items():
        key = attributes["score"]
        params[filter_by] = expected_score[key]

    response = client.get("/scores", query_string=params)

    assert response.status_code == 200
    assert len(response.json) > 0

    expected_score_visited = False
    for score in response.json:
        if score["id"] == expected_score["id"]:
            expected_score_visited = True

            assert score["player"] == expected_player
            assert score["beatmap"] == expected_beatmap

        # might as well throw in some extra checks
        for key in expected_score:
            assert key in score

    assert expected_score_visited


# TODO: pagination tests might be better as a separate set of unit
# tests, so that this case can be checked for all similar endpoints
def test_get_scores_with_limit_and_page(client):
    TOP_LIMIT = 6  # must be less than the amount of completed scores
    PAGED_LIMIT = 2  # must be no more than half of TOP_LIMIT

    response_top = client.get(
        "/scores", query_string={"limit": TOP_LIMIT}
    )

    assert response_top.status_code == 200
    assert len(response_top.json) == TOP_LIMIT

    response_paged = client.get(
        "/scores", query_string={"limit": PAGED_LIMIT, "page": 1}
    )

    assert response_paged.status_code == 200
    assert len(response_paged.json) == PAGED_LIMIT

    # not 100% sure this equality will just work™ yet but we'll see
    assert response_paged.json == response_top.json[PAGED_LIMIT:PAGED_LIMIT*2]


@pytest.mark.parametrize(
    "filter_by, value", (
        ("player", 1),  # chatot should have no scores
        ("beatmap", 1),  # beatmap doesn't exist
        ("mods", 2048),  # auto mod can't be submitted
        ("grade", "F"),  # failed scores excluded by default
    )
)
def test_get_scores_with_empty_result(client, filter_by, value):
    response = client.get("/scores", query_string={filter_by: value})

    assert response.status_code == 200
    assert response.json == []
