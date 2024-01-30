import base64
import os
import socket
import subprocess
from moviepy.editor import *

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

    # Scaling
    vid = VideoFileClip("videos\\" + video)

    w = vid.w
    h = vid.h

    max_res = int(request.args.get("resolution"))
    if h > max_res:
        w = round(w/(h/max_res))
        h = max_res

    master_key_base64 = "zFdeCYgaRA26pe8dEfhjSQ=="  # Replace with your actual master key
    master_salt_base64 = "dNf0fXBAOfiEBhYrb8k="  # Replace with your actual master salt

    subprocess.call(
        f"ffmpeg -re -i videos/{video} -vf scale={w}:{h} -map 0:v -c:v libx264 -preset ultrafast -tune zerolatency -b:v 1500k -f rtp"
        f" -srtp_in_suite SRTP_AES128_CM_HMAC_SHA1_80 -srtp_out_suite SRTP_AES128_CM_HMAC_SHA1_80"
        f" -srtp_in_params {base64.b64decode(master_key_base64).hex()}:{base64.b64decode(master_salt_base64).hex()}"
        f" -srtp_out_params {base64.b64decode(master_key_base64).hex()}:{base64.b64decode(master_salt_base64).hex()}"
        f" rtp://{ip_address}:{video_port} -map 0:a -c:a libopus -b:a 128k -f rtp rtp://{ip_address}:{audio_port}",
        shell=True
    )

    return "Playing video..."


@app.route("/get-sdp")
def get_sdp():
    video = request.args.get("video-name")
    ip_address = request.args.get("ip-address")

    print_out("Sending sdp to " + request.remote_addr)

    sdp_file = "server-temp\\" + video
    if not os.path.exists(sdp_file + ".sdp"):
        print("Generating sdp...")
        # Set your encryption parameters
        master_key_base64 = "zFdeCYgaRA26pe8dEfhjSQ=="  # Replace with your actual master key
        master_salt_base64 = "dNf0fXBAOfiEBhYrb8k="  # Replace with your actual master salt

        # Modify the subprocess call to generate SDP with encryption options
        subprocess.call(
            f"ffmpeg -re -i videos/{video} -map 0:v -c:v libx264 -preset ultrafast -tune zerolatency -b:v 1500k -f rtp"
            f" -srtp_in_suite SRTP_AES128_CM_HMAC_SHA1_80 -srtp_out_suite SRTP_AES128_CM_HMAC_SHA1_80"
            f" -srtp_in_params {base64.b64decode(master_key_base64).hex()}:{base64.b64decode(master_salt_base64).hex()}"
            f" -srtp_out_params {base64.b64decode(master_key_base64).hex()}:{base64.b64decode(master_salt_base64).hex()}"
            f" rtp://{ip_address}:{video_port} -map 0:a -c:a libopus -b:a 128k -f rtp rtp://{ip_address}:{audio_port}"
            f" -f sdp > {sdp_file}.sdp 2> {sdp_file}.txt",
            shell=True
)

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
