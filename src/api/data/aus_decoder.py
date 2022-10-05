import os
from typing import List

import cv2 as cv
import pandas as pd
import numpy as np
import mediapipe as mp


class Aus_Decoder:

    def __init__(self):
        def split_emotion_aus(row):
            try:
                return [int(el) for el in row.strip().replace(" ", "").split('+')]
            except AttributeError:
                return np.nan

        self.curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.df_emotions = pd.read_csv(os.path.join(self.curr_dir, 'dict_emotions.csv'), index_col='emotion')
        self.df_emotions['aus'] = self.df_emotions['aus'].apply(split_emotion_aus)
        self.df_aus = pd.read_csv(os.path.join(self.curr_dir, 'dict_aus.csv'), index_col='au')
        self.df_ldmk = pd.read_csv(
            os.path.join(self.curr_dir, 'dict_landmarks.csv'),
            index_col=0
        )
        self.df_ldmk['landmarks'] = self.df_ldmk['landmarks'].apply(
            lambda ldmk: np.unique(
                np.array(
                    ldmk.split(',')
                ).astype(np.float16)
            ) if pd.notnull(ldmk) else np.nan
        )

    def get_feeling_payload(self, feeling_label):
        feeling = self.df_emotions.loc[feeling_label].to_dict()
        payload = {
            'feeling': feeling_label,
            'feeling_description': feeling['description'],
            'aus': feeling['aus'],
            'aus_descriptions': {},
        }
        for au in feeling['aus']:
            payload['aus_descriptions'][au] = self.df_aus.loc[au]['description']

        return payload

    def get_all_feelings_payload(self):
        payload = {
            'aus': [int(el) for el in self.df_aus.index.values],
            'aus_descriptions': {},
            'feelings': list(self.df_emotions.index.values),
            'feelings_description': {},
        }

        for au in self.df_aus.index:
            payload['aus_descriptions'][au] = self.df_aus.loc[au]['description']

        for emotion in self.df_emotions.index:
            payload['feelings_description'][emotion] = self.df_emotions.loc[emotion]['description']

        return payload

    def get_landmarks_from_aus(self, aus: List[int]):
        ldmks = np.array([])
        for au in aus:
            ldmks = np.append(ldmks, self.df_ldmk.loc[au, 'landmarks'])
        ldmks = np.unique(ldmks)
        return ldmks

    @staticmethod
    def get_feeling_img(img_cv, landmarks: List[int]):
        mp_face_mesh = mp.solutions.face_mesh
        # mp_drawing = mp.solutions.drawing_utils
        # drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        # mp_drawing_styles = mp.solutions.drawing_styles
        with mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
        ) as face_mesh:
            height, width, _ = img_cv.shape
            # Convert the BGR image to RGB before processing.
            results = face_mesh.process(cv.cvtColor(img_cv, cv.COLOR_BGR2RGB))
            # Print and draw face mesh landmarks on the image.
            if not results.multi_face_landmarks:
                return None
            face_landmarks = results.multi_face_landmarks[0]  # Using first face detected only

            for ldmk in landmarks:
                if pd.isnull(ldmk):
                    continue
                ldmk = int(ldmk)

                pt1 = face_landmarks.landmark[ldmk]
                x = int(pt1.x * width)
                y = int(pt1.y * height)
                cv.circle(img_cv, (x, y), 5, (100, 100, 0), -1)
                cv.putText(img_cv, str(ldmk), (x, y), 1, 1, (0, 0, 0))
            return img_cv
