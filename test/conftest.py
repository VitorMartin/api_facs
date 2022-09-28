from src.api.handler import Handler
from src.config import Config
from main import create_app

import pytest


@pytest.fixture(scope='module')
def config():
    yield Config(env=Config.AVAILABLE_ENV_TEST)


@pytest.fixture(scope='module')
def handler(config):
    yield Handler(config=config)


@pytest.fixture(scope='module')
def client(config, handler):
    app = create_app(config, handler)
    with app.test_client() as client:
        with app.app_context():
            yield client
