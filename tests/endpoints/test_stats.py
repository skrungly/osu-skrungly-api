

def test_get_global_stats(client):
    response = client.get("/stats")

    assert response.status_code == 200

    expected_result = {
        "tscore": 45178791,
        "rscore": 28919771,
        "pp": 939,
        "plays": 13,
        "playtime": 1593,
        "total_hits": 8950,
    }

    for key, value in expected_result.items():
        assert response.json[key] == value


def test_bad_method_global_stats(client):
    for method in (client.post, client.put, client.delete):
        assert method("/stats").status_code == 405
