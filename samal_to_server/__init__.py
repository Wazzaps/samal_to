from flask import Flask, Response
import os
from samal_to_server.solve import solve
import json

app = Flask(__name__, static_url_path='/static')

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/')
def hello():
    return app.send_static_file('index.html')


@app.route('/api/v1/solve')
def solve_endpoint():
    req = json.load(open('./samal_to_server/example_req.json', 'rb'))
    return Response(
        json.dumps(solve(req['people'], req['settings'], req['shifts'])),
        mimetype='application/json'
    )
