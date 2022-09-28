"""
Modulo main. Ponto de entrada para a aplicação.
"""


from src.config import Config
from src.api.handler import Handler

import sys

from flask import Flask, request, send_file, json
from flask_api.status import *


config = Config()
app = Flask(config.API_NAME)
handler = Handler(config)
print(f'Python version: {sys.version_info}')
print(config.to_dict())


def create_app():
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


if __name__ == '__main__':
    create_app()
    app.run(host=config.HOST, port=config.PORT, debug=config.FLASK_DEBUG)
