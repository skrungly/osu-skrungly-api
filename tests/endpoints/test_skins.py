import pytest

from io import BytesIO

EXAMPLE_SKIN_NAME = "tests.osk"


@pytest.mark.parametrize("player", ("3", "shinx"))
class TestValidPlayer:

    def test_skin_missing_by_default(self, client, player):
        missing_response = client.get(f"/players/{player}/skin")
        assert missing_response.status_code == 404

    def test_upload_and_delete_skin(
        self,
        client,
        authorized_client,
        csrf_headers,
        example_skin,
        player
    ):
        # try to upload the basic skin with valid authentication
        form_data = {"file": (BytesIO(example_skin), EXAMPLE_SKIN_NAME)}

        put_response = authorized_client.put(
            f"/players/{player}/skin",
            headers=csrf_headers,
            data=form_data,
            buffered=True,
            content_type="multipart/form-data"
        )

        assert put_response.status_code == 204

        # now fetch the skin from an arbitrary client
        get_response = client.get(f"/players/{player}/skin")

        assert get_response.status_code == 200
        assert get_response.data == example_skin
        assert EXAMPLE_SKIN_NAME in get_response.headers["Content-Disposition"]

        # try to delete the skin from an unauthorized client
        unauth_delete_response = client.delete(f"/players/{player}/skin")

        assert unauth_delete_response.status_code == 401

        # then check that we can delete the skin with authorization
        auth_delete_response = authorized_client.delete(
            f"/players/{player}/skin", headers=csrf_headers
        )

        assert auth_delete_response.status_code == 204

        # and now it should be gone!
        deleted_get_response = client.get(f"/players/{player}/skin")

        assert deleted_get_response.status_code == 404

    def test_upload_skin_without_auth(self, client, example_skin, player):
        form_data = {"file": (BytesIO(example_skin), EXAMPLE_SKIN_NAME)}

        put_response = client.put(
            f"/players/{player}/skin",
            data=form_data,
            buffered=True,
            content_type="multipart/form-data"
        )

        assert put_response.status_code == 401
