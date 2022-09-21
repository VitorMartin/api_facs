import argparse
import os
import sys


class Config:
    AVAILABLE_ENV_PROD = 'prod'
    AVAILABLE_ENV_DEV = 'dev'
    AVAILABLE_ENV_TEST = 'test'

    def __init__(self, env: str = AVAILABLE_ENV_PROD):
        print(sys.argv)
        self.VERSION = '0.0'
        self.ENV = env

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '--version', '-v', action='version', version=self.VERSION, help='API\'s current version.'
        )
        self.parser.add_argument('--port', '-p', help='Port for the API host.')
        if env in [self.AVAILABLE_ENV_PROD, self.AVAILABLE_ENV_DEV]:
            self.args = self.parser.parse_args()
        elif env == self.AVAILABLE_ENV_TEST:
            if '_jb_pytest_runner.py' in sys.argv[0]:  # Checking how the test is being called
                self.parser.add_argument('src')
            self.args = self.parser.parse_args()

        self.API_NAME = 'API_FACS'

        self.PROTOCOL = 'http'
        self.HOST = '127.0.0.1'

        self.PORT = '8000' if self.args.port is None else self.args.port

        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.MOCK_DIR = os.path.join(
            self.ROOT_DIR, '..', 'mock_data'
        )

        self.AU_MODEL_IMG_SIZE = 224


    def to_dict(self):
        return {
            'api_name': self.API_NAME,
            'env': self.ENV,
            'version': self.VERSION,
            'protocol': self.PROTOCOL,
            'host': self.HOST,
            'port': self.PORT,
            'au_model_img_size': self.AU_MODEL_IMG_SIZE,
        }
