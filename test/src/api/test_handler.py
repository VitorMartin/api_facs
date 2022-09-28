from src.config import Config

from flask_api.status import *
from flask.testing import FlaskClient



class Test_Handler:
    def test_get_home(self, config: Config, client: FlaskClient):
        # Actual
        act_res = client.get('/')

        # Expected
        exp_res = config.to_dict()
        exp_res['msg'] = 'Welcome to our FACS API!'

        # Test
        assert act_res.status_code == HTTP_200_OK
        assert act_res.json == exp_res

    def test_post_feeling(self, client: FlaskClient, img_bytes: bytes):
        # Actual
        act_res = client.post(
            '/feeling',
            data=img_bytes,
            mimetype='image/jpeg'
        )
        act_json = act_res.json
        assert 'predict_time' in act_json  # Checking if key exists before changing it
        act_json['predict_time'] = 0  # Predict time will never be the same

        # Expected
        exp_res = {
            'aus': [
                6,
                12
            ],
            'aus_descriptions': {
                '6': 'Cheek Raiser',
                '12': 'Lip Corner Puller'
            },
            'feeling': 'happy',
            'feeling_accuracy': 100.0,
            'feeling_description': 'Cheek Raiser, Lip Corner Puller',
            'predict_time': 0
        }

        # Test
        assert act_res.status_code == HTTP_200_OK
        assert act_json == exp_res

    def test_post_feeling_image(self, client: FlaskClient, img_bytes: bytes):
        # Actual
        act_res = client.post(
            '/feeling/img',
            data=img_bytes,
            mimetype='image/jpeg'
        )

        # Test
        assert act_res.status_code == HTTP_200_OK
        assert act_res.mimetype == 'image/jpeg'

    def test_get_feeling_all(self, client: FlaskClient):
        # Actual
        act_res = client.get('/feeling/all')

        # Expected
        exp_res = {
            'aus': [
                1,   2,  4,  5,  6,  7,  9, 10, 11, 12,
                13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                33, 34, 35, 36, 37, 38, 39, 41, 42, 43,
                44, 45, 46, 51, 52, 53, 54, 55, 56, 57,
                58, 61, 62, 63, 64
            ],
            'aus_descriptions': {
                '1': 'Inner Brow Raiser', '2': 'Outer Brow Raiser', '4': 'Brow Lowerer', '5': 'Upper Lid Raiser',
                '6': 'Cheek Raiser', '7': 'Lid Tightener', '9': 'Nose Wrinkler', '10': 'Upper Lip Raiser',
                '11': 'Nasolabial Deepener', '12': 'Lip Corner Puller', '13': 'Cheek Puffer', '14': 'Dimpler',
                '15': 'Lip Corner Depressor', '16': 'Lower Lip Depressor', '17': 'Chin Raiser', '18': 'Lip Puckerer',
                '19': 'Língua para Fora', '20': 'Lip stretcher', '21': 'Endurecedor de Pescoço -- Platysma',
                '22': 'Lip Funneler', '23': 'Lip Tightener', '24': 'Lip Pressor', '25': 'Lips part', '26': 'Jaw Drop',
                '27': 'Mouth Stretch', '28': 'Lip Suck', '29': 'Projeção de Mandíbula',
                '30': 'Movimentação Lateral da Mandíbula', '31': 'Jaw Clencher -- Masseter',
                '32': 'Mordida do Lábio', '33': 'Inflar de Bochecha', '34': 'Bufar de Bochecha',
                '35': 'Sucção de Bochecha', '36': 'Arqueamento da Língua', '37': 'Limpeza do Lábio',
                '38': 'Dilatador das Narinas', '39': 'Compressor das Narinas', '41': 'Lid droop', '42': 'Slit',
                '43': 'Eyes Closed', '44': 'Squint', '45': 'Blink', '46': 'Wink', '51': 'Head Turn Left',
                '52': 'Head Turn Right', '53': 'Head Up', '54': 'Head Down', '55': 'Head Tilt Left',
                '56': 'Head Tilt Right', '57': 'Head Forward', '58': 'Head Back', '61': 'Eyes Turn Left',
                '62': 'Eyes Turn Right', '63': 'Eyes Up', '64': 'Eyes Down'
            },
            'feelings': [
                'happy', 'sad', 'surprise', 'fear', 'angry', 'disgust', 'contempt', 'neutral'
            ],
            'feelings_description': {
                'angry': 'Brow Lowerer, Upper Lid Raiser, Lid Tightener, Lip Tightener',
                'contempt': 'Lip Corner Puller, Dimpler',
                'disgust': 'Nose Wrinkler, Lip Corner Depressor, Lower Lip Depressor',
                'fear': 'Inner Brow Raiser, Outer Brow Raiser, Brow Lowerer, Upper Lid Raiser, Lid Tightener, '
                        'Lip Stretcher, Jaw Drop',
                'happy': 'Cheek Raiser, Lip Corner Puller',
                'neutral': "No facial actions",
                'sad': 'Inner Brow Raiser, Brow Lowerer, Lip Corner Depressor',
                'surprise': 'Inner Brow Raiser, Outer Brow Raiser, Upper Lid Raiser, Jaw Drop'
            }
        }

        # Test
        assert act_res.status_code == HTTP_200_OK
        assert act_res.json == exp_res
