import socket
import subprocess
import time

import requests

import Utils

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


def play_video(sdp_loc, port, video, resolution):
    print("Playing video")
    subprocess.Popen("ffplay -protocol_whitelist file,rtp,udp " + sdp_loc, shell=True)
    requests.get("http://" + server_ip + ":" + str(
        port) + "/play-video?video-name=" + video + "&ip-address=" + get_ip_address() + "&resolution=" + str(resolution))


def get_sdp(video, port, resolution):
    print("Loading video, please wait...")
    sdp_str = requests.get("http://" + server_ip + ":" + str(port) + "/get-sdp?video-name=" + video + "&ip-address=" +
                           server_ip).text

    sdp_loc = "client-temp\\" + video + ".sdp"
    sdp_file = open(sdp_loc, "w")
    sdp_file.write(sdp_str)
    sdp_file.close()

    play_video(sdp_loc, port, video, resolution)


def video_chose_menu(port):
    try:
        video_list = requests.get("http://" + server_ip + ":" + str(port) + "/get-videos").text.split(",")
    except requests.exceptions.ConnectionError:
        Utils.print_err("A connection to " + server_ip + ":" + str(port) + " could not be created, is it correct?")
        return

    if check_error(video_list):
        return

    i = 1
    for video in video_list:
        print(str(i) + ". " + video_list[i - 1])

        i += 1

    print("Enter a video name (with file extension)")
    print("-----------------------------------")
    video = input("> ")
    print("")
    print("Enter a resolution (eg. '1080' or '720') (Leave blank for default)")
    print("-----------------------------------")
    try:
        resolution = input("> ")
        if resolution == "":
            resolution = 1080
        else:
            resolution = int(resolution)
    except:
        Utils.print_err("Your input is not an integer. Defaulting to 1080")
        resolution = 1080

    get_sdp(video.lower(), port, resolution)


def setup_client(port):
    global server_ip
    print("""What is the servers ip?

-----------------------------------""")
    server_ip = input("> ")

    video_chose_menu(port)


def check_error(str):
    if "Internal Server Error" in str:
        Utils.print_error("A connection could not be created. Please try again.")

    return "Internal Server Error" in str
