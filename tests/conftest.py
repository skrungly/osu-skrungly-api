import functools
import json
from pathlib import Path

import pytest

from app import app


@pytest.fixture()
def flask_app(tmp_path):
    app._data_dir = tmp_path
    yield app


@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture()
def auth_tokens(client):
    response = client.post(
        "/auth/login",
        json={
            "name": "shinx",
            "password": "test1234",
            "cookie": False
        }
    )

    return response.json


@pytest.fixture()
def authorized_client(client):
    client.post(
        "/auth/login",
        json={
            "name": "shinx",
            "password": "test1234",
            "cookie": True
        }
    )

    return client


@pytest.fixture()
def csrf_headers(authorized_client):
    csrf_cookie = authorized_client.get_cookie("csrf_access_token")
    return {"X-CSRF-TOKEN": csrf_cookie.value}


@pytest.fixture(scope="session")
def expected_data():
    expected_data_path = Path("tests") / "data" / "expected"

    @functools.cache
    def _expected_data(data_label):
        json_path = (expected_data_path / data_label).with_suffix(".json")
        with open(json_path) as json_file:
            return json.load(json_file)

    return _expected_data


@pytest.fixture(scope="session")
def read_example_file():
    data_path = Path("tests") / "data"

    @functools.cache
    def _example_file(file_path):
        # the skin should only be a few kB in size so let's just read it
        with open(data_path / file_path, "rb") as example_file:
            return example_file.read()

    return _example_file
