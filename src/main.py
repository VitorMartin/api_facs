"""
Modulo main. Ponto de entrada para a aplicação.
"""


import sys

from src.config import Config
from src.api.server import Server


if __name__ == '__main__':
    print(f'Python version: {sys.version_info}')
    config = Config(env=Config.AVAILABLE_ENV_DEV)
    print(config.to_dict())
    server = Server(config=config)
    server.run()
