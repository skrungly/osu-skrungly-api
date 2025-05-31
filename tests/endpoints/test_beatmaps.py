import pytest

# testing individual maps (/maps/...)

APOPLEXY_ = {
    "id": 811675,
    "set_id": 370340,
    "status": 2,
    "md5": "f8483b44ffbbc86603f486aad3ceaa0d",
    "artist": "CENOB1TE",
    "title": "Onslaught",
    "version": "apoplexy_",
    "creator": "Irreversible",
    "filename": "CENOB1TE - Onslaught (Irreversible) [apoplexy_].osu",
    "last_update": "2015-10-26T19:35:41",
    "total_length": 199,
    "max_combo": 1002,
    "frozen": 0,
    "plays": 5,
    "passes": 2,
    "mode": 0,
    "bpm": 140.0,
    "cs": 4.0,
    "ar": 9.3,
    "od": 8.5,
    "hp": 7.0,
    "diff": 5.989,
}


def test_get_ranked_bancho_beatmap(client):
    response = client.get("/maps/811675")

    assert response.status_code == 200

    for key, value in APOPLEXY_.items():
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

def test_get_ranked_bancho_mapset(client):
    response = client.get("/mapsets/370340")

    assert response.status_code == 200

    # mapset has 5 difficulties
    assert len(response.json) == 5

    for map_data in response.json:
        assert all(key in map_data for key in APOPLEXY_)


@pytest.mark.parametrize("set_id", ["", "/2", "/aaaaa"])
def test_get_inexistent_bancho_mapset(client, set_id):
    response = client.get(f"/mapsets{set_id}")

    assert response.status_code == 404


def test_bad_methods_mapsets(client):
    for http_method in (client.post, client.put, client.delete):
        assert http_method("/mapsets/370340").status_code == 405
