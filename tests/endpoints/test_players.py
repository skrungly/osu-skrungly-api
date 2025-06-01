import pytest

EXAMPLE_PLAYER = {
    "id": 3,
    "name": "shinx",
    "safe_name": "shinx",
    "priv": 31879,
    "country": "gb",
    "creation_time": 1748697194,
    "latest_activity": 1748811533,
    "preferred_mode": 0,
    "userpage_content": "hello!",
}

EXAMPLE_STATS = {
    "id": 3,
    "mode": 0,
    "tscore": 106149900,
    "rscore": 92370390,
    "pp": 449,
    "plays": 9,
    "playtime": 1335,
    "acc": 97.367,
    "max_combo": 1932,
    "total_hits": 4730,
    "replay_views": 0,
    "xh_count": 0,
    "x_count": 0,
    "sh_count": 0,
    "s_count": 2,
    "a_count": 2,
}


@pytest.mark.parametrize("player_id", ["/3", "/shinx"])
class TestValidPlayer:

    def test_get_valid_player(self, client, player_id):
        response = client.get(f"/players{player_id}")

        assert response.status_code == 200

        for key, value in EXAMPLE_PLAYER.items():
            assert response.json[key] == value

        assert "stats" in response.json

        # since we're not comparing the dictionary directly, we should at
        # least make sure the whole database row isn't being returned:
        assert "email" not in response.json
        assert "pw_bcrypt" not in response.json

        response_stats = response.json["stats"]
        example_stats_response = None

        # check that all of the stats lists satisfy the expected schema
        for stats in response_stats:
            assert all(key in stats for key in EXAMPLE_STATS)

            # keep track of the stats we want to check more thoroughly
            if stats["mode"] == EXAMPLE_STATS["mode"]:
                example_stats_response = stats

        # we should have come across the stats for the example by now
        assert example_stats_response is not None

        for key, value in EXAMPLE_STATS.items():
            assert example_stats_response[key] == value

    @pytest.mark.parametrize("mode_id", [0, "osu", 3, "mania"])
    def test_get_valid_player_stats(self, client, player_id, mode_id):
        response = client.get(
            f"/players{player_id}/stats",
            query_string={
                "mode": mode_id
            }
        )

        assert response.status_code == 200

        for key in EXAMPLE_STATS:
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
