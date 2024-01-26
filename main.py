from flask import Flask
from waitress import serve
from flask import request

app = Flask(__name__)


@app.route("/play-video")
def hello_world():
    video = request.args.get("video")
    print("Recieved request for video " + video)
    return "Play video " + video


serve(app, host='0.0.0.0', port=5000, threads=1)
