# ./src/api/server.py


import config

from sanic import Sanic, Request, json


app = Sanic(name=config.HOST)


@app.get('/')
async def get_home_handler(req: Request):
    res = config.to_dict()
    res['msg'] = 'Welcome to our FACS API!'
    return json(res)


@app.get('all')
async def get_all_handler(req: Request):
    return json({'msg': 'get_all'})


@app.get('feeling')
async def get_feeling_handler(req: Request):
    return json({'msg': 'get_feeling'})


@app.get('model')
async def get_model_handler(req: Request):
    return json({'msg': 'get_model'})


@app.post('image')
async def post_image_handler(req: Request):
    return json({})


def run(host: str = config.HOST, port: int = config.PORT):
    app.run(host=host, port=port)
