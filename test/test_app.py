import pytest

from src.config import Config

from flask_api.status import *
from flask.testing import FlaskClient


class Test_Environment:
    def test_python_version(self, config: Config):
        major, minor, patch = config.PYTHON_VERSION.split('.')
        assert major == '3'
        assert minor == '7'

    def test_config(self, config: Config):
        # Actual
        act_config = config.to_dict()
        major, minor, patch = act_config['python_version'].split('.')
        act_config['python_version'] = major + '.' + minor

        # Expected
        exp_config = {
            'api_name': 'API_FACS',
            'api_version': '0.0',
            'au_model_img_size': 224,
            'env': 'test',
            'flask_debug': True,
            'host': '127.0.0.1',
            'port': '8000',
            'protocol': 'http',
            'python_version': '3.7'
        }

        # Test
        assert act_config == exp_config


class Test_Endpoints:
    def test_home_endpoint(self, client: FlaskClient):
        res = client.get('/')
        assert res.status_code == HTTP_200_OK
        assert res.mimetype == 'application/json'

    def test_feeling_endpoint(self, config: Config, client: FlaskClient, img_bytes: bytes):
        res = client.post(
            '/feeling',
            data=img_bytes,
            mimetype='image/jpeg'
        )
        assert res.status_code == HTTP_200_OK
        assert res.mimetype == 'application/json'

    def test_feeling_img_endpoint(self, client: FlaskClient, img_bytes: bytes):
        res = client.post(
            '/feeling/img',
            data=img_bytes,
            mimetype='image/jpeg'
        )
        assert res.status_code == HTTP_200_OK
        assert res.mimetype == 'image/jpeg'

    def test_feeling_all_endpoint(self, client: FlaskClient):
        res = client.get('/feeling/all')
        assert res.status_code == HTTP_200_OK
        assert res.mimetype == 'application/json'


class Test_Endpoints_Exceptions:
    @pytest.mark.skip(reason="Fix front-end compatibility before testing edge cases.")
    def test_feeling_endpoint_bad_request(self, client: FlaskClient):
        res = client.post(
            '/feeling',
            data={'wrong': 'data'},
            mimetype='application/json'
        )
        assert res.status_code == HTTP_400_BAD_REQUEST
        assert res.json == {'msg': 'Invalid MIME type provided. Send an image file instead.'}
