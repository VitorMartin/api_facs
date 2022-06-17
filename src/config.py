import os


API_NAME = 'API FACS'
VERSION = '0.0'

PROTOCOL = 'http'
HOST = 'localhost'
PORT = 8080

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_DIR = os.path.join(
    ROOT_DIR, '..', 'mock_data'
)


def to_dict():
    return {
        'api_name': API_NAME,
        'version': VERSION,
        'protocol': PROTOCOL,
        'host': HOST,
        'port': PORT,
    }
