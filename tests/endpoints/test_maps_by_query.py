import pytest

MAPS_ENDPOINT = "/maps"

# (sort by ...) => <field>
BASIC_SORT_OPTIONS = {
    "plays": "plays",
    "passes": "passes",  # default?
    "diff": "diff",
    "length": "total_length",
    # "combo": "max_combo",  # prod db has bad data for combo right now
}

BASIC_FILTER_OPTIONS = ("frozen", "mode", "set_id")

# (status alias) => (expected status values)
STATUS_ALIASES = {
    "pending": {0},
    "ranked": {2},
    "approved": {3},
    "qualified": {4},
    "loved": {5},
    "leaderboard": {2, 3, 4, 5},
    "all": {0, 2, 3, 4, 5}
}


@pytest.mark.parametrize("sort_by", BASIC_SORT_OPTIONS)
def test_get_maps_sorted_basic(client, sort_by):
    params = {"sort": sort_by}

    response = client.get(MAPS_ENDPOINT, query_string=params)

    assert response.status_code == 200
    assert len(response.json) > 0

    # now make sure the result is sorted correctly
    previous_value = None
    db_column = BASIC_SORT_OPTIONS[sort_by]
    for map_data in response.json:
        if previous_value is not None:
            assert previous_value >= map_data[db_column]

        previous_value = map_data[db_column]


def test_get_maps_sorted_by_popular(client):
    params = {"sort": "popular"}

    response = client.get(MAPS_ENDPOINT, query_string=params)

    assert response.status_code == 200
    assert len(response.json) > 0

    previous_value = None
    for map_data in response.json:
        assert "popularity" in map_data

        if previous_value is not None:
            assert previous_value >= map_data["popularity"]

        previous_value = map_data["popularity"]


@pytest.mark.parametrize("filter_by", BASIC_FILTER_OPTIONS)
def test_get_maps_filtered_basic(client, expected_data, filter_by):
    # for each filter, choose a value to filter by such that the
    # expected (serialised) map will show up in each case.
    expected_map = expected_data("beatmap")
    expected_value = expected_map[filter_by]

    response = client.get(
        MAPS_ENDPOINT,
        query_string={
            filter_by: expected_value,
            "limit": 1000,  # TODO: allow limit = 0
        }
    )

    assert response.status_code == 200
    assert len(response.json) > 0

    expected_map_visited = False
    for map_data in response.json:
        # using map md5 as it's better as a unique identifier than id
        # (since id could be non-unique with custom map submissions)
        if map_data["md5"] == expected_map["md5"]:
            expected_map_visited = True

        assert map_data[filter_by] == expected_value

    assert expected_map_visited


@pytest.mark.parametrize("status", (None, 0, 2, 3, 4, 5, *STATUS_ALIASES))
def test_get_maps_filtered_by_status(client, status):
    params = None if status is None else {"status": status}

    response = client.get(MAPS_ENDPOINT, query_string=params)

    assert response.status_code == 200

    if status is None:
        status = "all"

    expected_statuses = STATUS_ALIASES.get(status) or {status}

    for map_data in response.json:
        assert map_data["status"] in expected_statuses


def test_get_maps_with_compound_query(client, expected_data):
    expected_map = expected_data("beatmap")

    # collect some filters that still match the expected map
    params = {"limit": 100}
    for filter_by in BASIC_FILTER_OPTIONS:
        params[filter_by] = expected_map[filter_by]

    response = client.get(MAPS_ENDPOINT, query_string=params)

    assert response.status_code == 200
    assert len(response.json) > 0

    expected_map_visited = False
    for map_data in response.json:
        if map_data["md5"] == expected_map["md5"]:
            expected_map_visited = True

        for key in expected_map:
            assert key in map_data

    assert expected_map_visited


@pytest.mark.parametrize(
    "filter_by, value", (
        ("mode", 4),  # no maps for relax (maybe this should be 422?)
        ("set_id", 0),  # no mapset with this id
    )
)
def test_get_maps_with_empty_result(client, filter_by, value):
    response = client.get(MAPS_ENDPOINT, query_string={filter_by: value})

    assert response.status_code == 200
    assert response.json == []
