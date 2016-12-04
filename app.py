from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return app.send_static_file('index.html')

@app.route('/<path:the_path>')
def all_other_routes(the_path):
    return app.send_static_file('index.html')