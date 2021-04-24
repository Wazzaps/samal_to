from flask import Flask
import os

app = Flask(__name__, static_url_path='/static')
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'samal_to.sqlite'),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/')
def hello():
    return app.send_static_file('index.html')
