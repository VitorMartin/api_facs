# ./src/api/server.py
from src.api.data.aus_decoder import Aus_Decoder
from src.config import Config

import cv2 as cv
import numpy as np
import tensorflow as tf
import os
from keras.models import Model
from keras.utils import img_to_array
from keras.utils.image_utils import smart_resize

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
        if(feeling == "happy"):
            labels = ["6,12"]
            au_list = []
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            model = tf.keras.models.load_model(f'{curr_dir}/models/model_aus_happy.h5')
            img_keras = img_to_array(img_cv)
            img_keras = np.expand_dims(img_keras, axis=0)
            img_keras = smart_resize(img_keras, (224, 224))
            prediction = model.predict(img_keras)[0]
            prediction_idx = np.argmax(prediction)
            prediction_label = labels[prediction_idx].split(",")
            for au in prediction_label: (au_list.append(int(au)))
        
        elif(feeling == "sad"):
            labels = ["1,4,15", "1,4,15,17"]
            au_list = []
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            model = tf.keras.models.load_model(f'{curr_dir}/models/model_aus_sadness.h5')
            img_keras = img_to_array(img_cv)
            img_keras = np.expand_dims(img_keras, axis=0)
            img_keras = smart_resize(img_keras, (224, 224))
            prediction = model.predict(img_keras)[0]
            prediction_idx = np.argmax(prediction)
            prediction_label = labels[prediction_idx].split(",")
            for au in prediction_label: (au_list.append(int(au)))
        
        elif(feeling == "disgust"):
            labels = ["9,17", "10,17"]
            au_list = []
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            model = tf.keras.models.load_model(f'{curr_dir}/models/model_aus_disgust.h5')
            img_keras = img_to_array(img_cv)
            img_keras = np.expand_dims(img_keras, axis=0)
            img_keras = smart_resize(img_keras, (224, 224))
            prediction = model.predict(img_keras)[0]
            prediction_idx = np.argmax(prediction)
            prediction_label = labels[prediction_idx].split(",")
            for au in prediction_label: (au_list.append(int(au)))
        
        elif(feeling == "fear"):
            labels = ["1,2,4,5", "1,2,4,5,25"]
            au_list = []
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            model = tf.keras.models.load_model(f'{curr_dir}/models/model_aus_fear.h5')
            img_keras = img_to_array(img_cv)
            img_keras = np.expand_dims(img_keras, axis=0)
            img_keras = smart_resize(img_keras, (224, 224))
            prediction = model.predict(img_keras)[0]
            prediction_idx = np.argmax(prediction)
            prediction_label = labels[prediction_idx].split(",")
            for au in prediction_label: (au_list.append(int(au)))
        
        elif(feeling == "angry"):
            labels = ["4,5,7,17,23", "4,5,7,17,24"]
            au_list = []
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            model = tf.keras.models.load_model(f'{curr_dir}/models/model_aus_angry.h5')
            img_keras = img_to_array(img_cv)
            img_keras = np.expand_dims(img_keras, axis=0)
            img_keras = smart_resize(img_keras, (224, 224))
            prediction = model.predict(img_keras)[0]
            prediction_idx = np.argmax(prediction)
            prediction_label = labels[prediction_idx].split(",")
            for au in prediction_label: (au_list.append(int(au)))
        
        elif(feeling == "surprise"):
            labels = ["1,2,5,26", "1,2,26"]
            au_list = []
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            model = tf.keras.models.load_model(f'{curr_dir}/models/model_aus_surprise.h5')
            img_keras = img_to_array(img_cv)
            img_keras = np.expand_dims(img_keras, axis=0)
            img_keras = smart_resize(img_keras, (224, 224))
            prediction = model.predict(img_keras)[0]
            prediction_idx = np.argmax(prediction)
            prediction_label = labels[prediction_idx].split(",")
            for au in prediction_label: (au_list.append(int(au)))
        
        else:
            labels = ["0"]
            au_list = []
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            model = tf.keras.models.load_model(f'{curr_dir}/models/model_aus_neutral.h5')
            img_keras = img_to_array(img_cv)
            img_keras = np.expand_dims(img_keras, axis=0)
            img_keras = smart_resize(img_keras, (224, 224))
            prediction = model.predict(img_keras)[0]
            prediction_idx = np.argmax(prediction)
            prediction_label = labels[prediction_idx].split(",")
            for au in prediction_label: (au_list.append(int(au)))
          
        aus_payload = aus_decoder.get_feeling_payload(feeling)
        aus_payload.pop('feeling')
        aus = au_list #aus_payload['aus']

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
