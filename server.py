import os
import socket

from flask import Flask, request
from waitress import serve

from Utils import print_out

app = Flask(__name__)


def get_ip_address():
    try:
        # This will return the primary IP address associated with the machine
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
        return None


@app.route("/get-videos")
def get_video_list():
    #video = request.args.get("video")

    print_out("Sending video list to " + request.remote_addr)
    video_list = []
    for video in os.listdir("./videos"):
        video_list.append(video.title())

    return ",".join(video_list)


def setup_server():
    print("Running server on " + get_ip_address())

    serve(app, host='0.0.0.0', port=5000, threads=1)