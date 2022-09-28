import sys


class Test_environment:
    def test_python_version(self):
        py_ver = sys.version_info[:2]
        assert py_ver == (3, 7)

    def test_config(self, config):
        assert config.to_dict() == {
            'api_name': 'API_FACS',
            'au_model_img_size': 224,
            'env': 'test',
            'flask_debug': True,
            'host': '127.0.0.1',
            'port': '8000',
            'protocol': 'http',
            'version': '0.0'
        }
