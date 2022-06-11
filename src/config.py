API_NAME = 'API FACS'
VERSION = '0.0'

PROTOCOL = 'http'
HOST = 'localhost'
PORT = 8080


def to_dict():
    return {
        'api_name': API_NAME,
        'version': VERSION,
        'protocol': PROTOCOL,
        'host': HOST,
        'port': PORT,
    }
