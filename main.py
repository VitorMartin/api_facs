"""
Modulo main. Ponto de entrada para a aplicação.
"""


import sys

from flask import Flask

from src.config import Config
from src.api.handler import Handler


config = Config(env=Config.AVAILABLE_ENV_PROD)
app = Flask(config.API_NAME)
handler = Handler(config)
print(f'Python version: {sys.version_info}')
print(config.to_dict())


@app.route('/', methods=['GET'])
def get_home_endpoint():
    return handler.get_home_handler()


@app.route('/feeling', methods=['POST'])
def post_feeling_endpoint():
    return 'handler.post_feeling_handler()'


@app.route('/feeling/img', methods=['POST'])
def post_image_endpoint():
    return handler.post_feeling_image_handler()


@app.route('/feeling/all', methods=['GET'])
def get_feeling_all():
    return handler.get_feeling_all_handler()


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.FLASK_DEBUG)
