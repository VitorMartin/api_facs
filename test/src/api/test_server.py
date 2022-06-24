import pytest

from src.config import Config
from src.api.server import Server


class Test_Server:
    @pytest.fixture(scope='class')
    def server(self):
        return Server(config=Config(env=Config.AVAILABLE_ENV_TEST))

    @pytest.fixture(scope='class')
    def app(self, server):
        return server.app

    @pytest.mark.asyncio
    async def test_get_home(self, server, app):
        config = Config(env=Config.AVAILABLE_ENV_TEST)

        # Actual
        req, res = await app.asgi_client.get("/")

        # Expected
        exp_res = config.to_dict()
        exp_res['msg'] = 'Welcome to our FACS API!'

        # Test
        assert req.method.lower() == "get"
        assert res.status == 200
        assert res.json == exp_res

    @pytest.mark.asyncio
    async def test_post_feeling(self, app):
        # Actual
        req, res = await app.asgi_client.post("/feeling")

        # Expected
        exp_res = {
            "feeling": "joy",
            "action_units": [
                "AU6",
                "AU12"
            ],
            "model_used": "modelo_1",
            "accuracy": 0.9051,
            "avg_predict_time": 1051
        }

        # Test
        assert req.method.lower() == "post"
        assert res.status == 200
        assert res.json == exp_res

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
