import pytest


def test_get_valid_score(client, expected_data):
    expected_score = expected_data("score")

    response = client.get("/scores/15")

    assert response.status_code == 200

    for key, value in expected_score.items():
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
