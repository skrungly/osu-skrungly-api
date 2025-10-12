import pytest


def test_get_ranked_bancho_mapset(client, expected_data):
    expected_map = expected_data("beatmap")

    response = client.get(f"/mapsets/{expected_map['set_id']}")

    assert response.status_code == 200
    assert len(response.json) == 5  # mapset has 5 difficulties

    for map_data in response.json:
        assert all(key in map_data for key in expected_map)


@pytest.mark.parametrize("set_id", ["2", "aaaaa"])
def test_get_inexistent_bancho_mapset(client, set_id):
    response = client.get(f"/mapsets/{set_id}")

    assert response.status_code == 404


def test_bad_methods_mapsets(client, expected_data):
    set_id = expected_data("beatmap")["set_id"]

    for http_method in (client.post, client.put, client.delete):
        assert http_method(f"/mapsets/{set_id}").status_code == 405
