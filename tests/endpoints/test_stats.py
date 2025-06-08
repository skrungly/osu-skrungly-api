

def test_get_global_stats(client, expected_data):
    expected_stats = expected_data("global_stats")

    response = client.get("/stats")

    assert response.status_code == 200

    for key, value in expected_stats.items():
        assert response.json[key] == value


def test_bad_method_global_stats(client):
    for method in (client.post, client.put, client.delete):
        assert method("/stats").status_code == 405
