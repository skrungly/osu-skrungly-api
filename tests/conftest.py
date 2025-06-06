import pytest
from dotenv import load_dotenv

from app import app

load_dotenv(".env.testing")


@pytest.fixture()
def flask_app():
    yield app


@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture()
def get(client):
    return client.get


@pytest.fixture()
def post(client):
    return client.post


@pytest.fixture()
def put(client):
    return client.put


@pytest.fixture()
def delete(client):
    return client.delete
