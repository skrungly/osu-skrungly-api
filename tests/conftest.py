import functools
import json
from pathlib import Path

import pytest

from app import app


@pytest.fixture()
def flask_app():
    yield app


@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture(scope="session")
def expected_data():
    expected_data_path = Path("tests") / "data" / "expected"

    @functools.cache
    def _expected_data(data_label):
        json_path = (expected_data_path / data_label).with_suffix(".json")
        with open(json_path) as json_file:
            return json.load(json_file)

    return _expected_data
