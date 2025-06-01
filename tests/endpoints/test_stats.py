EXAMPLE_STATS = {
    "tscore": 117302691,
    "rscore": 98658541,
    "pp": 1060,
    "plays": 17,
    "playtime": 2117,
    "total_hits": 11456,
}


def test_get_global_stats(client):
    response = client.get("/stats")

    assert response.status_code == 200

    for key, value in EXAMPLE_STATS.items():
        assert response.json[key] == value


def test_bad_method_global_stats(client):
    for method in (client.post, client.put, client.delete):
        assert method("/stats").status_code == 405
