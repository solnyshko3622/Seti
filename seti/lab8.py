import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/folder")
def index():
    return str([item for item in os.listdir(os.getcwd()) if os.path.isdir(item)])

if __name__ == "__main__":
    app.run(host='localhost', port=4567)

