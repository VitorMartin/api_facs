import os
from sanic.response import json
import numpy as np
import cv2 as cv
import pytest

from src.config import Config
from src.api.server import Server


class Test_Server:
    config = Config(env=Config.AVAILABLE_ENV_TEST)


    @pytest.fixture(scope='class')
    def server(self):
        return Server(config=self.config)

    @pytest.fixture(scope='class')
    def app(self, server):
        return server.app

    @pytest.mark.asyncio
    async def test_get_home(self, server, app):
        # Actual
        req, res = await app.asgi_client.get("/")

        # Expected
        exp_res = self.config.to_dict()
        exp_res['msg'] = 'Welcome to our FACS API!'

        # Test
        assert req.method.lower() == "get"
        assert res.status == 200
        assert res.json == exp_res

    @pytest.mark.asyncio
    async def test_post_feeling(self, app):
        # Actual
        with open(os.path.join(self.config.ROOT_DIR, '..', 'mock_data', 'happy_placeholder_1.jpeg'), 'rb') as file:
            img_bytes = file.read()
        req, res = await app.asgi_client.post("/feeling", data=img_bytes)
        act_res = res.json

        # Expected
        exp_res = {
            "feeling": "happy",
            "action_units": [
                999
            ],
            "feeling_accuracy": 100.0,
            "predict_time": act_res['predict_time']
        }

        # Test
        assert req.method.lower() == "post"
        assert res.status == 200
        assert act_res == exp_res

    @pytest.mark.asyncio
    async def test_post_feeling_image(self, app):
        # Actual
        req, res = await app.asgi_client.post("/feeling/img")

        # Test
        assert req.method.lower() == "post"
        assert res.status == 200

    @pytest.mark.asyncio
    async def test_get_feeling_all(self, app):
        # Actual
        req, res = await app.asgi_client.get("/feeling/all")

        # Expected
        exp_res = {
            "anger": ["AU4", "AU5", "AU7", "AU23"],
            "contempt": ["AU12", "AU14"],
            "disgust": ["AU9", "AU15", "AU16"],
            "fear": ["AU1", "AU2", "AU4", "AU5", "AU7", "AU20", "AU26"],
            "joy": ["AU6", "AU12"],
            "sadness": ["AU1", "AU4", "AU15"],
            "surprise": ["AU1", "AU2", "AU5", "AU26"]
        }

        # Test
        assert req.method.lower() == "get"
        assert res.status == 200
        assert res.json == exp_res

    @pytest.mark.asyncio
    async def test_get_models(self, app):
        # Actual
        req, res = await app.asgi_client.get("/models")

        # Expected
        exp_res = {
            "models": [
                {
                    "nome": "model_1",
                    "accuracy": 0.9051,
                    "avg_predict_time": 1051
                },
                {
                    "nome": "model_2",
                    "accuracy": 0.9733,
                    "avg_predict_time": 2496
                },
                {
                    "nome": "model_3",
                    "accuracy": 0.8522,
                    "avg_predict_time": 4754
                }
            ]
        }

        # Test
        assert req.method.lower() == "get"
        assert res.status == 200
        assert res.json == exp_res
