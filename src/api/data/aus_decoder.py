import os
import pandas as pd
import numpy as np


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
