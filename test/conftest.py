from src.api.handler import Handler
from src.config import Config
from main import create_app

import os
import pytest
from flask.testing import FlaskClient


@pytest.fixture(scope='module')
def config() -> Config:
    yield Config(env=Config.AVAILABLE_ENV_TEST)


@pytest.fixture(scope='module')
def handler(config) -> Handler:
    yield Handler(config=config)


@pytest.fixture(scope='module')
def img_bytes(config) -> bytes:
    with open(os.path.join(config.MOCK_DIR, 'happy_placeholder_1.jpg'), 'rb') as file:
        img_bytes = file.read()
    yield img_bytes


@pytest.fixture(scope='module')
def img_no_face_bytes(config) -> bytes:
    with open(os.path.join(config.MOCK_DIR, 'face_placeholder_1.jpg'), 'rb') as file:
        img_bytes = file.read()
    yield img_bytes


@pytest.fixture(scope='module')
def client(config, handler) -> FlaskClient:
    app = create_app(config, handler)
    with app.test_client() as client:
        with app.app_context():
            yield client
