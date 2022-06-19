# ./src/api/server.py
import src.config as config
import os

from sanic import Sanic, response, Request
from sanic_cors import CORS


class Server:
    app: Sanic


    def __init__(self):
        self.app = Sanic(name=config.API_NAME)
        CORS(self.app)


        @self.app.get('/')
        async def get_home_handler(req: Request):
            res = config.to_dict()
            res['msg'] = 'Welcome to our FACS API!'
            return response.json(res)


        @self.app.post('/feeling')
        async def get_feeling_handler(req: Request):
            return response.json({
                'feeling': 'joy',
                'action_units': ['AU6', 'AU12'],
                'model_used': 'modelo_1',
                'accuracy': .9051,
                'avg_predict_time': 1051
            })


        @self.app.post('/feeling/img')
        async def post_image_handler(req: Request):
            return await response.file(
                os.path.join(config.MOCK_DIR, 'face_predict_placeholder_1.jpg'),
                filename='img_predict.jpg'
            )


        @self.app.get('/feeling/all')
        async def get_all_handler(req: Request):
            return response.json({
                'anger': ['AU4', 'AU5', 'AU7', 'AU23'],
                'contempt': ['AU12', 'AU14'],
                'disgust': ['AU9', 'AU15', 'AU16'],
                'fear': ['AU1', 'AU2', 'AU4', 'AU5', 'AU7', 'AU20', 'AU26'],
                'joy': ['AU6', 'AU12'],
                'sadness': ['AU1', 'AU4', 'AU15'],
                'surprise': ['AU1', 'AU2', 'AU5', 'AU26'],
            })


        @self.app.get('/models')
        async def get_model_handler(req: Request):
            return response.json({
                'models': [
                    {
                        'nome': 'model_1',
                        'accuracy': 0.9051,
                        'avg_predict_time': 1051,
                    },
                    {
                        'nome': 'model_2',
                        'accuracy': 0.9733,
                        'avg_predict_time': 2496,
                    },
                    {
                        'nome': 'model_3',
                        'accuracy': 0.8522,
                        'avg_predict_time': 4754,
                    }
                ]
            })


    def run(self, host: str = config.HOST, port: int = config.PORT):
        self.app.run(host=host, port=port)
