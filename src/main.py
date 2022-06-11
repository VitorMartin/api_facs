"""
Modulo main. Ponto de entrada para a aplicação.
"""


import sys

from api import server


if __name__ == '__main__':
    print(f'Python version: {sys.version_info}')
    server.run()
