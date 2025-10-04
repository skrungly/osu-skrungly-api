import pytest


# test endpoints without valid authorisation

def test_get_identity_without_auth(client):
    response = client.get("/auth/identity")

    assert response.status_code == 200
    assert response.json["identity"] is None


@pytest.mark.parametrize(
    "name, password", (
        ("shinx", "aaaaaaa"),  # invalid password
        ("aaaaaaa", "test1234"),  # invalid user
    )
)
def test_invalid_login(client, name, password):
    response = client.post(
        "/auth/login",
        json={
            "name": name,
            "password": password,
            "cookie": False
        }
    )

    assert response.status_code == 401


# now properly test auth endpoints using header-based tokens first

def test_valid_auth_identity_without_cookies(client, auth_tokens):
    assert auth_tokens["identity"] == "3"
    assert "access_token" in auth_tokens
    assert "refresh_token" in auth_tokens

    response = client.get(
        "/auth/identity",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )

    assert response.status_code == 200
    assert response.json["identity"] == "3"


def test_valid_auth_refresh_without_cookies(client, auth_tokens):
    refresh_response = client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {auth_tokens['refresh_token']}"}
    )

    assert refresh_response.status_code == 200
    assert refresh_response.json["identity"] == "3"

    new_access_token = refresh_response.json["access_token"]
    assert new_access_token != auth_tokens["access_token"]

    id_response = client.get(
        "/auth/identity",
        headers={"Authorization": f"Bearer {new_access_token}"},
    )

    assert id_response.status_code == 200
    assert id_response.json["identity"] == "3"


def test_valid_auth_logout_without_cookies(client, auth_tokens):
    auth_header = {"Authorization": f"Bearer {auth_tokens['access_token']}"}

    logout_response = client.delete("/auth/logout", headers=auth_header)

    assert logout_response.status_code == 200
    assert logout_response.json["identity"] is None

    # we should now get an appropriate response for expired tokens
    id_response = client.get("/auth/identity", headers=auth_header)
    refresh_response = client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {auth_tokens['refresh_token']}"}
    )

    assert id_response.status_code == 401
    assert refresh_response.status_code == 401


# the following tests are the exact same as those above, just with
# cookie-based tokens rather than explicit header-based tokens.

def test_valid_auth_identity_with_cookies(authorized_client):
    assert authorized_client.get_cookie("access_token_cookie")
    assert authorized_client.get_cookie("csrf_access_token")
    assert authorized_client.get_cookie("refresh_token_cookie")
    assert authorized_client.get_cookie("csrf_refresh_token")

    response = authorized_client.get("/auth/identity")

    assert response.status_code == 200
    assert response.json["identity"] == "3"


def test_valid_auth_refresh_with_cookies(authorized_client):
    old_access_cookie = authorized_client.get_cookie("access_token_cookie")

    # ensure that we can't refresh tokens without CSRF
    invalid_response = authorized_client.post("/auth/refresh")

    assert invalid_response.status_code == 401

    # now attempt a genuine request with CSRF
    csrf_cookie = authorized_client.get_cookie("csrf_refresh_token")
    refresh_response = authorized_client.post(
        "/auth/refresh",
        headers={"X-CSRF-TOKEN": csrf_cookie.value}
    )

    new_access_cookie = authorized_client.get_cookie("access_token_cookie")

    assert refresh_response.status_code == 200
    assert refresh_response.json["identity"] == "3"
    assert new_access_cookie.value != old_access_cookie.value

    id_response = authorized_client.get("/auth/identity")

    assert id_response.status_code == 200
    assert id_response.json["identity"] == "3"


def test_valid_auth_logout_with_cookies(authorized_client):
    # we'll try some explicit authentication with these afterwards
    # to verify that they have been invalidated properly
    access_cookie = authorized_client.get_cookie("access_token_cookie")
    refresh_cookie = authorized_client.get_cookie("refresh_token_cookie")

    # like with refreshing tokens, let's test without CSRF
    invalid_response = authorized_client.delete("/auth/logout")

    assert invalid_response.status_code == 401

    # now try a genuine logout attempt with CSRF
    csrf_cookie = authorized_client.get_cookie("csrf_access_token")
    logout_response = authorized_client.delete(
        "/auth/logout",
        headers={"X-CSRF-TOKEN": csrf_cookie.value}
    )

    assert logout_response.status_code == 200
    assert logout_response.json["identity"] is None

    # the api should clear the client cookies
    id_response = authorized_client.get("/auth/identity")

    assert id_response.status_code == 200
    assert id_response.json["identity"] is None

    # now explicitly verify that the tokens are invalid
    id_response = authorized_client.get(
        "/auth/identity",
        headers={"Authorization": f"Bearer {access_cookie.value}"}
    )

    refresh_response = authorized_client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_cookie.value}"}
    )

    assert id_response.status_code == 401
    assert refresh_response.status_code == 401
