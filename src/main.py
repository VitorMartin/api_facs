"""
Modulo main. Ponto de entrada para a aplicação.
"""


import sys

from api.server import Server

if __name__ == '__main__':
    print(f'Python version: {sys.version_info}')
    server = Server()
    server.run()
