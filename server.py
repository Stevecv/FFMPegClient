import os
import socket
import subprocess

from flask import Flask, request
from waitress import serve

from Utils import print_out

app = Flask(__name__)

video_port = 5008
audio_port = 5010


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
    print_out("Sending video list to " + request.remote_addr)
    video_list = []
    for video in os.listdir("./videos"):
        video_list.append(video.title())

    return ",".join(video_list)


@app.route("/play-video")
def play_video():
    print_out("Playing video for " + request.remote_addr)
    video = request.args.get("video-name")
    ip_address = request.args.get("ip-address")
    subprocess.call(
        "ffmpeg -re -i \"videos\\" + video + "\" -map 0:v -c:v libx264 -preset ultrafast -tune zerolatency -b:v 1500k -f rtp rtp://" + ip_address + ":" + str(
            video_port) + " -map 0:a -c:a libopus -b:a 128k -f rtp rtp://" + ip_address + ":" + str(audio_port) + "",
        shell=True)

    return "Playing video..."


@app.route("/get-sdp")
def get_sdp():
    video = request.args.get("video-name")
    ip_address = request.args.get("ip-address")

    print_out("Sending sdp to " + request.remote_addr)

    sdp_file = "server-temp\\" + video
    if not os.path.exists(sdp_file + ".sdp"):
        print("Generating sdp...")
        subprocess.call(
            "ffmpeg -re -i \"videos\\" + video + "\" -map 0:v -c:v libx264 -preset ultrafast -tune zerolatency -b:v 1500k -f rtp rtp://" + ip_address + ":" + str(
                video_port) + " -map 0:a -c:a libopus -b:a 128k -f rtp rtp://" + ip_address + ":" + str(
                audio_port) + " -sdp_file " + sdp_file + ".sdp 2> " + sdp_file + ".txt", shell=True)

    f = open(sdp_file + ".sdp", "r")
    return f.read()


def setup_server(port):
    global video_port
    global audio_port

    print("Running server on " + get_ip_address())

    print("Using video port: " + str(video_port))
    print("Using audio port: " + str(audio_port))

    serve(app, host='0.0.0.0', port=port, threads=1)
    print("Serving")
