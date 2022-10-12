"""
Modulo main. Ponto de entrada para a aplicação.
"""

from flask_cors import CORS
from src.config import Config
from src.api.handler import Handler

import sys

from flask import Flask, request, json
from flask_api.status import *


def create_app(config: Config, handler: Handler):
    app = Flask(config.API_NAME)
    CORS(app)

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

        try:
            res = handler.post_feeling_handler(request)
        except ValueError as err:
            return app.response_class(
                response=json.dumps({'msg': err.args[0]}),
                status=HTTP_400_BAD_REQUEST,
                mimetype='application/json'
            )

        return res

    @app.route('/feeling/all', methods=['GET'])
    def get_feeling_all():
        return handler.get_feeling_all_handler()

    return app


# ==== MAIN ==== #
def main():
    config = Config()
    handler = Handler(config)
    app = create_app(config, handler)
    print(f'Python version: {sys.version_info}')
    print(config.to_dict())
    app.run(host=config.HOST, port=config.PORT, debug=config.FLASK_DEBUG)


if __name__ == '__main__':
    main()
