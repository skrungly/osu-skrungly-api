import pytest

EXAMPLE_SCORE = {
    "id": 15,
    "map_md5": "12e14d24b09da2dc7b067dfd11497b69",
    "score": 69738770,
    "pp": 137.277,
    "acc": 98.198,
    "max_combo": 1932,
    "mods": 0,
    "n300": 1224,
    "n100": 34,
    "n50": 0,
    "nmiss": 0,
    "ngeki": 165,
    "nkatu": 28,
    "grade": "S",
    "status": 2,
    "mode": 0,
    "play_time": "2025-06-01T20:34:18",
    "time_elapsed": 297431,
    "client_flags": 0,
    "userid": 3,
    "perfect": 1,
    "online_checksum": "7288178df28b46fa1d8aaa1674e78b5a"
}


def test_get_valid_score(client):
    response = client.get("/scores/15")

    assert response.status_code == 200

    for key, value in EXAMPLE_SCORE.items():
        assert response.json[key] == value


@pytest.mark.parametrize("score_id", ["", "/99999999"])
def test_get_inexistent_score(client, score_id):
    response = client.get(f"/scores{score_id}")

    assert response.status_code == 404


def test_get_invalid_score(client):
    response = client.get("/scores/aaaaa")

    assert response.status_code == 422


def test_bad_methods_scores(client):
    for http_method in (client.post, client.put, client.delete):
        assert http_method("/scores/15").status_code == 405
