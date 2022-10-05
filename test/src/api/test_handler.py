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
            mimetype='image/jpg'
        )
        act_json = act_res.json

        # Checking if key exists before changing it
        assert 'predict_time' in act_json
        assert type(act_json['predict_time']) is int
        assert act_json['predict_time'] >= 0
        act_json['predict_time'] = 0

        # Checking if key exists before changing it
        assert 'image' in act_json
        assert type(act_json['image']) is str
        # Checking if string is in "list" format
        assert act_json['image'].startswith('[') and act_json['image'].endswith(']')
        # Irrelevant to test actual image bytes
        act_json['image'] = 0

        # Expected
        exp_res = {
            'aus': [6, 12],
            'aus_descriptions': {'12': 'Lip corner puller', '6': 'Cheek raiser'},
            'feeling': 'happy',
            'feeling_accuracy': 100.0,
            'feeling_description': 'Cheek raiser and lip corner puller',
            'predict_time': 0,
            'image': 0
        }

        # Test
        assert act_res.status_code == HTTP_200_OK
        assert act_json == exp_res

    def test_get_feeling_all(self, client: FlaskClient):
        # Actual
        act_res = client.get('/feeling/all')

        # Expected
        exp_res = {
            'aus': [
                0,   1,  2,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 50, 51, 52, 53, 54, 55,
                56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 80, 81, 82, 83, 84, 85, 91, 92,
                97, 98
            ],
            'aus_descriptions': {
                '0': 'Neutral face', '1': 'Inner brow raiser', '10': 'Upper lip raiser', '11': 'Nasolabial deepener',
                '12': 'Lip corner puller', '13': 'Sharp lip puller', '14': 'Dimpler', '15': 'Lip corner depressor',
                '16': 'Lower lip depressor', '17': 'Chin raiser', '18': 'Lip pucker', '19': 'Tongue show',
                '2': 'Outer brow raiser', '20': 'Lip stretcher', '21': 'Neck tightener', '22': 'Lip funneler',
                '23': 'Lip tightener', '24': 'Lip pressor', '25': 'Lips part', '26': 'Jaw drop', '27': 'Mouth stretch',
                '28': 'Lip suck', '29': 'Jaw thrust', '30': 'Jaw sideways', '31': 'Jaw clencher', '32': 'Lip bite',
                '33': 'Cheek blow', '34': 'Cheek puff', '35': 'Cheek suck', '36': 'Tongue bulge', '37': 'Lip wipe',
                '38': 'Nostril dilator', '39': 'Nostril compressor', '4': 'Brow lowerer', '40': 'Sniff',
                '41': 'Lid droop', '42': 'Slit', '43': 'Eyes closed', '44': 'Squint', '45': 'Blink', '46': 'Wink',
                '5': 'Upper lid raiser', '50': 'Speech', '51': 'Head turn left', '52': 'Head turn right',
                '53': 'Head up', '54': 'Head down', '55': 'Head tilt left', '56': 'Head tilt right',
                '57': 'Head forward', '58': 'Head back', '59': 'Head shake up and down', '6': 'Cheek raiser',
                '60': 'Head shake side to side', '61': 'Eyes turn left', '62': 'Eyes turn right', '63': 'Eyes up',
                '64': 'Eyes down', '65': 'Walleye', '66': 'Cross-eye', '68': 'Upward rolling of eyes',
                '69': 'Head or eyes look at other person', '7': 'Lid tightener', '70': 'Brows and forehead not visible',
                '71': 'Eyes not visible', '72': 'Lower face not visible', '73': 'Entire face not visible',
                '74': 'Unscorable', '8': 'Lips toward each other', '80': 'Swallow', '81': 'Chewing',
                '82': 'Shoulder shrug', '83': 'Head upward and to the side', '84': 'Head shake back and forth',
                '85': 'Head nod up and down', '9': 'Nose wrinkler', '91': 'Flash', '92': 'Partial flash',
                '97': 'Shiver/tremble', '98': 'Fast up-down look'
            },
            'feelings': [
                'angry', 'contempt', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise'
            ],
            'feelings_description': {
                'angry': 'Brow lowerer, upper lid raiser, lid tightener and lip tightener',
                'contempt': 'Lip corner puller and dimpler',
                'disgust': 'Nose wrinkler, lip corner depressor, ' 'lower lip depressor',
                'fear': 'Inner brow raiser, outer brow raiser, brow lowerer, upper lid raiser, lid tightener, '
                        'lip stretcher and jaw drop',
                'happy': 'Cheek raiser and lip corner puller',
                'neutral': 'Neutral face',
                'sad': 'Inner brow raiser, brow lowerer and lip ' 'corner depressor',
                'surprise': 'Inner brow raiser, outer brow raiser, ' 'upper lid raiser and jaw drop'
            }
        }

        # Test
        assert act_res.status_code == HTTP_200_OK
        assert act_res.json == exp_res


class Test_Handler_Exceptions:
    def test_post_feeling_no_face_detected(self, client: FlaskClient, img_no_face_bytes: bytes):
        act_res = client.post(
            '/feeling',
            data=img_no_face_bytes,
            mimetype='image/jpeg'
        )
        assert act_res.status_code == HTTP_400_BAD_REQUEST
        assert act_res.json == {
            'msg': 'Face could not be detected. Please confirm that the picture is a face photo '
                   'or consider to set enforce_detection param to False.'
        }
