# ./src/api/server.py
import config
import os

from sanic import Sanic, response, Request
from src.api.cors import add_cors_headers
from src.api.options import setup_options


class Server:
    app: Sanic


    def __init__(self):
        self.app = Sanic(name=config.API_NAME)
        self.app.register_listener(setup_options, 'before_server_start')
        self.app.register_middleware(add_cors_headers, 'response')


        @self.app.get('/')
        async def get_home_handler(req: Request):
            res = config.to_dict()
            res['msg'] = 'Welcome to our FACS API!'
            return response.json(res)


        @self.app.post('/feeling')
        async def get_feeling_handler(req: Request):
            return response.json({
                'joy': [6, 12],
            })


        @self.app.post('/feeling/image')
        async def post_image_handler(req: Request):
            return await response.file(
                os.path.join(config.MOCK_DIR, 'face_predict_placeholder_1.jpg'),
                filename='img_predict.jpg'
            )


        @self.app.get('/feeling/all')
        async def get_all_handler(req: Request):
            return response.json({
                'anger': [4, 5, 7, 23],
                'contempt': [12, 14],
                'disgust': [9, 15, 16],
                'fear': [1, 2, 4, 5, 7, 20, 26],
                'joy': [6, 12],
                'sadness': [1, 4, 15],
                'surprise': [1, 2, 5, 26],
            })


        @self.app.get('/models')
        async def get_model_handler(req: Request):
            return response.json({
                'modelo_1': {
                    'accuracy': 0.9051,
                    'avg_predict_time': 1051,
                },
                'modelo_2': {
                    'accuracy': 0.9733,
                    'avg_predict_time': 2496,
                },
                'modelo_3': {
                    'accuracy': 0.8522,
                    'avg_predict_time': 4754,
                }
            })


    def run(self, host: str = config.HOST, port: int = config.PORT):
        self.app.run(host=host, port=port)
