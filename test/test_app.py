from src.config import Config


class Test_environment:
    def test_python_version(self, config: Config):
        major, minor, patch = config.PYTHON_VERSION.split('.')
        assert major == '3'
        assert minor == '7'

    def test_config(self, config):
        assert config.to_dict() == {
            'api_name': 'API_FACS',
            'api_version': '0.0',
            'au_model_img_size': 224,
            'env': 'test',
            'flask_debug': True,
            'host': '127.0.0.1',
            'port': '8000',
            'protocol': 'http',
            'python_version': '3.7.9'
        }
