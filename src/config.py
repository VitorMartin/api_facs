import argparse
import os


class Config:
    AVAILABLE_ENV_PROD = 'prod'
    AVAILABLE_ENV_DEV = 'dev'
    AVAILABLE_ENV_TEST = 'test'

    def __init__(self, env: str = AVAILABLE_ENV_PROD):
        self.VERSION = '0.0'
        self.ENV = env

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '--version', '-v', action='version', version=self.VERSION, help='API\'s current version.'
        )
        self.parser.add_argument('--port', '-p', help='Port for the API host.')
        if env in [self.AVAILABLE_ENV_PROD, self.AVAILABLE_ENV_DEV]:
            self.args = self.parser.parse_args([])
        elif env == self.AVAILABLE_ENV_TEST:
            self.args = self.parser.parse_args([])

        self.API_NAME = 'API_FACS'

        self.PROTOCOL = 'http'
        self.HOST = 'localhost'

        self.PORT = '8000' if self.args.port is None else self.args.port

        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.MOCK_DIR = os.path.join(
            self.ROOT_DIR, '..', 'mock_data'
        )


    def to_dict(self):
        return {
            'api_name': self.API_NAME,
            'env': self.ENV,
            'version': self.VERSION,
            'protocol': self.PROTOCOL,
            'host': self.HOST,
            'port': self.PORT,
        }
