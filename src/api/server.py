# ./src/api/server.py
from src.config import Config

import os
from sanic import Sanic, response, Request
from sanic_cors import CORS
import cv2 as cv
import numpy as np
from keras.models import load_model
from keras.utils import img_to_array
from keras.utils.image_utils import smart_resize
from time import time

class Server:
    app: Sanic


    def __init__(self, config: Config = None):
        self.config = Config() if config is None else config
        self.app = Sanic(name=self.config.API_NAME)
        CORS(self.app)


        @self.app.get('/')
        async def get_home_handler(req: Request):
            res = self.config.to_dict()
            res['msg'] = 'Welcome to our FACS API!'
            return response.json(res)


        @self.app.post('/feeling')
        async def get_feeling_handler(req: Request):
            from deepface import DeepFace  # Importando localmente, para nao conflitar com Pytest

            start_time = time()
            img_arr = np.fromstring(req.body, np.uint8)
            img_cv = cv.imdecode(img_arr, cv.IMREAD_COLOR)

            # Predict DeepFace
            df_predict = DeepFace.analyze(
                img_cv,
                actions=('emotion',),
                models={'emotion': DeepFace.build_model('Emotion')}
            )
            feeling = df_predict['dominant_emotion']

            # Predict AUs
            au_model = load_model(os.path.join(self.config.ROOT_DIR, 'au_detection_model.h5'))
            img_keras = img_to_array(img_cv)
            img_keras = np.expand_dims(img_keras, axis=0)
            img_keras = smart_resize(img_keras, (self.config.AU_MODEL_IMG_SIZE, self.config.AU_MODEL_IMG_SIZE))
            prediction = au_model.predict(img_keras)[0]
            mean = prediction.mean()
            std = prediction.std()
            prediction_classes = np.where(prediction > mean + std)[0]
            aus = {}
            for pred in prediction_classes:
                aus[int(pred)] = float(prediction[pred])

            predict_time = time() - start_time
            res = {
                'feeling': feeling,
                'action_units': aus,
                'feeling_accuracy': round(df_predict['emotion'][feeling], 2),
                'predict_time': round(predict_time * 1000),
            }
            return response.json(res)


        @self.app.post('/feeling/img')
        async def post_image_handler(req: Request):
            return await response.file(
                os.path.join(self.config.MOCK_DIR, 'face_predict_placeholder_1.jpg'),
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


    def run(self, host: str = None, port: int = None):
        host = self.config.HOST if host is None else host
        port = self.config.PORT if port is None else port

        self.app.run(
            host=host,
            port=port,
            debug=True if self.config.ENV == Config.AVAILABLE_ENV_DEV else False
        )
