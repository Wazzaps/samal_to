from flask import Flask, Response, request
from flask_cors import CORS
import os
from samal_to_server.solve import solve
import json

app = Flask(__name__, static_url_path='/static')
cors = CORS(app, resources={"/v1/*": {"origins": "*"}})

@app.route('/')
def hello():
    return app.send_static_file('index.html')


@app.route('/v1/solve', methods=["POST"])
def solve_endpoint():
    req = request.json
    return Response(
        json.dumps(solve(req['people'], req['settings'], req['shifts'])),
        mimetype='application/json'
    )
