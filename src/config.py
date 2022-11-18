import argparse
import os
import sys


class Config:
    AVAILABLE_ENV_PROD = 'prod'
    AVAILABLE_ENV_DEV = 'dev'
    AVAILABLE_ENV_TEST = 'test'

    def __init__(self, env: str = AVAILABLE_ENV_PROD):
        print(sys.argv)

        self.PYTHON_VERSION = sys.version.split(' ')[0]

        self.API_VERSION = '1.0'
        self.ENV = env

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '--version', '-v', action='version', version=self.API_VERSION, help='API\'s current version.'
        )
        self.parser.add_argument(
            '--port', '-p', help='Port for the API host.'
        )
        # Host option can't be "-h" because it is being used by the "--help" argument
        self.parser.add_argument(
            '--host', '-H', help='IP to host the API.'
        )
        if env in [self.AVAILABLE_ENV_PROD, self.AVAILABLE_ENV_DEV]:
            self.args = self.parser.parse_args()
        elif env == self.AVAILABLE_ENV_TEST:
            if '_jb_pytest_runner.py' in sys.argv[0]:  # Checking how the test is being called
                self.parser.add_argument('src')
            self.args = self.parser.parse_args()

        self.API_NAME = 'API_FACS'

        self.PROTOCOL = 'http'
        self.HOST = '0.0.0.0' if self.args.host is None else self.args.host
        self.PORT = '80' if self.args.port is None else self.args.port

        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.MOCK_DIR = os.path.join(
            self.ROOT_DIR, '..', 'mock_data'
        )

        self.AU_MODEL_IMG_SIZE = 224

        self.FLASK_DEBUG = False if self.ENV == self.AVAILABLE_ENV_PROD else True


    def to_dict(self):
        return {
            'api_name': self.API_NAME,
            'api_version': self.API_VERSION,
            'au_model_img_size': self.AU_MODEL_IMG_SIZE,
            'env': self.ENV,
            'flask_debug': self.FLASK_DEBUG,
            'host': self.HOST,
            'port': self.PORT,
            'protocol': self.PROTOCOL,
            'python_version': self.PYTHON_VERSION,
        }
