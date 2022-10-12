# ./src/api/server.py
from src.api.data.aus_decoder import Aus_Decoder
from src.config import Config

import cv2 as cv
import numpy as np

from time import time


class Handler:
    def __init__(self, config: Config = None):
        self.config = Config() if config is None else config


    @staticmethod
    def get_feeling_all_handler():
        return Aus_Decoder().get_all_feelings_payload()

    @staticmethod
    def post_feeling_handler(req):
        from deepface import DeepFace  # Importando localmente, para nao conflitar com Pytest
        aus_decoder = Aus_Decoder()

        start_time = time()

        img_arr = np.frombuffer(req.data, dtype=np.uint8)
        img_cv = cv.imdecode(img_arr, cv.IMREAD_COLOR)

        # Predict DeepFace
        df_predict = DeepFace.analyze(
            img_cv,
            actions=('emotion',),
            models={'emotion': DeepFace.build_model('Emotion')}
        )
        feeling = df_predict['dominant_emotion']

        # Predict AUs
        aus_payload = aus_decoder.get_feeling_payload(feeling)
        aus_payload.pop('feeling')
        aus = aus_payload['aus']

        # Draw AUs
        landmarks = aus_decoder.get_landmarks_from_aus(aus)
        img_landmarks = aus_decoder.get_feeling_img(img_cv, landmarks)
        # Transforming into image
        img_converted = cv.imencode('.jpg', img_landmarks)[1]

        predict_time = time() - start_time

        res = {
            'feeling': feeling,
            'feeling_accuracy': round(df_predict['emotion'][feeling], 2),
            'predict_time': round(predict_time * 1000),
            **aus_payload,
            'image': str(list(img_converted))
        }

        return res

    def get_home_handler(self):
        res = self.config.to_dict()
        res['msg'] = 'Welcome to our FACS API!'
        return res
