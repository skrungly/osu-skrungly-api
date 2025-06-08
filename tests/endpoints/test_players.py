import pytest


@pytest.mark.parametrize("player_id", ["/3", "/shinx"])
class TestValidPlayer:

    def test_get_valid_player(self, client, expected_data, player_id):
        expected_player = expected_data("player")
        expected_stats = expected_data("player_stats")

        response = client.get(f"/players{player_id}")

        assert response.status_code == 200

        for key, value in expected_player.items():
            assert response.json[key] == value

        assert "stats" in response.json

        # since we're not comparing the dictionary directly, we should at
        # least make sure the whole database row isn't being returned:
        assert "email" not in response.json
        assert "pw_bcrypt" not in response.json

        response_stats = response.json["stats"]
        expected_stats_in_response = None

        # check that all of the stats lists satisfy the expected schema
        for stats in response_stats:
            assert all(key in stats for key in expected_stats)

            # keep track of the stats we want to check more thoroughly
            if stats["mode"] == expected_stats["mode"]:
                expected_stats_in_response = stats

        # we should have come across the stats for the example by now
        assert expected_stats_in_response is not None

        for key, value in expected_stats.items():
            assert expected_stats_in_response[key] == value

    @pytest.mark.parametrize("mode_id", [0, "osu", 3, "mania"])
    def test_get_player_stats(self, client, expected_data, player_id, mode_id):
        expected_stats = expected_data("player_stats")

        response = client.get(
            f"/players{player_id}/stats",
            query_string={
                "mode": mode_id
            }
        )

        assert response.status_code == 200

        for key in expected_stats:
            assert key in response.json

    @pytest.mark.parametrize("mode_id", [1, 2, 4])
    def test_get_missing_player_stats(self, client, player_id, mode_id):
        response = client.get(
            f"/players{player_id}/stats",
            query_string={
                "mode": mode_id
            }
        )

        assert response.status_code == 404

    @pytest.mark.parametrize("mode_id", [100, "aaaaa", ""])
    def test_get_invalid_player_stats(self, client, player_id, mode_id):
        response = client.get(
            f"/players{player_id}/stats",
            query_string={
                "mode": mode_id
            }
        )

        assert response.status_code == 422

    def test_bad_methods_stats(self, client, player_id):
        for http_method in (client.post, client.put, client.delete):
            response = http_method(f"/players{player_id}/stats?mode=0")
            assert response.status_code == 405


@pytest.mark.parametrize("player_id", ["/2", "/aaaaa"])
def test_get_invalid_player(client, player_id):
    response = client.get(f"/players{player_id}")

    assert response.status_code == 404
