import pytest


# testing individual maps (/maps/...)

def test_get_ranked_bancho_beatmap(client, expected_data):
    expected_map = expected_data("beatmap")

    response = client.get("/maps/811675")

    assert response.status_code == 200

    for key, value in expected_map.items():
        assert response.json[key] == value


# there is no map with id 2 on bancho, so it should 404
@pytest.mark.parametrize("map_id", ["", "/2", "/aaaaa"])
def test_get_inexistent_bancho_beatmap(client, map_id):
    response = client.get(f"/maps{map_id}")

    assert response.status_code == 404


def test_bad_methods_beatmaps(client):
    for http_method in (client.post, client.put, client.delete):
        assert http_method("/maps/811675").status_code == 405


# testing mapsets (/mapsets/...)

def test_get_ranked_bancho_mapset(client, expected_data):
    expected_map = expected_data("beatmap")

    response = client.get("/mapsets/370340")

    assert response.status_code == 200
    assert len(response.json) == 5  # mapset has 5 difficulties

    for map_data in response.json:
        assert all(key in map_data for key in expected_map)


@pytest.mark.parametrize("set_id", ["", "/2", "/aaaaa"])
def test_get_inexistent_bancho_mapset(client, set_id):
    response = client.get(f"/mapsets{set_id}")

    assert response.status_code == 404


def test_bad_methods_mapsets(client):
    for http_method in (client.post, client.put, client.delete):
        assert http_method("/mapsets/370340").status_code == 405
