import pytest

from io import BytesIO

EXAMPLE_SKIN_NAME = "tests.osk"


@pytest.mark.parametrize("player", ("3", "shinx"))
@pytest.mark.parametrize(
    "endpoint, example_file", (
        ("skin", "tests.osk"),
        ("banner", "tests.jpg"),
    )
)
class TestValidPlayerUploads:

    def test_file_missing_by_default(
        self,
        client,
        player,
        endpoint,
        example_file
    ):
        missing_response = client.get(f"/players/{player}/{endpoint}")
        assert missing_response.status_code == 404

    def test_upload_and_delete_file(
        self,
        client,
        authorized_client,
        csrf_headers,
        player,
        endpoint,
        example_file,
        read_example_file,
    ):
        example_data = read_example_file(example_file)

        # try to upload the basic file with valid authentication
        form_data = {"file": (BytesIO(example_data), example_file)}

        put_response = authorized_client.put(
            f"/players/{player}/{endpoint}",
            headers=csrf_headers,
            data=form_data,
            buffered=True,
            content_type="multipart/form-data"
        )

        assert put_response.status_code == 204

        # now fetch the endpoint from an arbitrary client
        get_response = client.get(f"/players/{player}/{endpoint}")
        assert get_response.status_code == 200

        # the `skin` endpoint should return the .osz file with the
        # original filename intact.
        if endpoint == "skin":
            assert get_response.data == example_data
            assert example_file in get_response.headers["Content-Disposition"]

        # try to delete the file from an unauthorized client
        unauth_delete_response = client.delete(f"/players/{player}/{endpoint}")
        assert unauth_delete_response.status_code == 401

        # then check that we can delete the file with authorization
        auth_delete_response = authorized_client.delete(
            f"/players/{player}/{endpoint}", headers=csrf_headers
        )

        assert auth_delete_response.status_code == 204

        # and now it should be gone!
        deleted_get_response = client.get(f"/players/{player}/{endpoint}")
        assert deleted_get_response.status_code == 404

    def test_upload_file_without_auth(
        self,
        client,
        player,
        endpoint,
        example_file,
        read_example_file,
    ):
        example_data = read_example_file(example_file)

        # try to upload the basic file with valid authentication
        form_data = {"file": (BytesIO(example_data), example_file)}

        put_response = client.put(
            f"/players/{player}/{endpoint}",
            data=form_data,
            buffered=True,
            content_type="multipart/form-data"
        )

        assert put_response.status_code == 401
