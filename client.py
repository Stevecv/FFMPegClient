import socket
import subprocess
import time

import requests

server_ip = ""

def get_ip_address():
    try:
        # This will return the primary IP address associated with the machine
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
        return None


def play_video(sdp_loc, port, video):
    print("Playing video")
    requests.get("http://" + server_ip + ":" + str(port) + "/play-video?video-name=" + video + "&ip-address=" + get_ip_address())
    subprocess.call("ffplay -protocol_whitelist file,rtp,udp " + sdp_loc, shell=True)



def get_sdp(video, port):
    print("Loading video, please wait...")
    print(server_ip)
    sdp_str = requests.get("http://" + server_ip + ":" + str(port) + "/get-sdp?video-name=" + video + "&ip-address=" +
                           server_ip).text

    sdp_loc = "client-temp\\" + video + ".sdp"
    sdp_file = open(sdp_loc, "w")
    sdp_file.write(sdp_str)
    sdp_file.close()

    play_video(sdp_loc, port, video)


def video_chose_menu(port):
    video_list = requests.get("http://" + server_ip + ":" + str(port) + "/get-videos").text.split(",")

    i = 1
    for video in video_list:
        print(str(i) + ". " + video_list[i-1])

        i += 1

    print("Enter a video name (with file extension)")
    print("-----------------------------------")
    video = input("> ")
    get_sdp(video, port)


def setup_client(port):
    global server_ip
    print("""What is the servers ip?

-----------------------------------""")
    server_ip = input("> ")

    video_chose_menu(port)


