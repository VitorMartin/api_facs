"""
Modulo main. Ponto de entrada para a aplicação.
"""


from src.config import Config
from src.api.handler import Handler

import sys

from flask import Flask, request, send_file, json
from flask_api.status import *


def create_app(config: Config, handler: Handler):
    app = Flask(config.API_NAME)


    @app.route('/', methods=['GET'])
    def get_home_endpoint():
        return handler.get_home_handler()


    @app.route('/feeling', methods=['POST'])
    def post_feeling_endpoint():
        if not request.mimetype.startswith('image/'):
            return app.response_class(
                response=json.dumps({'msg': 'Invalid MIME type provided. Send an image file instead.'}),
                status=HTTP_400_BAD_REQUEST,
                mimetype='application/json'
            )

        return handler.post_feeling_handler(request)


    @app.route('/feeling/img', methods=['POST'])
    def post_image_endpoint():
        return send_file(
            handler.post_feeling_image_handler()
        )


    @app.route('/feeling/all', methods=['GET'])
    def get_feeling_all():
        return handler.get_feeling_all_handler()


    return app


if __name__ == '__main__':
    _config = Config()
    _handler = Handler(_config)
    _app = create_app(_config, _handler)
    print(f'Python version: {sys.version_info}')
    print(_config.to_dict())
    _app.run(host=_config.HOST, port=_config.PORT, debug=_config.FLASK_DEBUG)
