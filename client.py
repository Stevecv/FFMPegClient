import subprocess

import requests

server_ip = ""


def play_video(sdp_loc):
    print("Playing video")
    subprocess.call("ffplay -protocol_whitelist file,rtp,udp -i " + sdp_loc, shell=True)
    print("Played video")


def get_sdp(video, port):
    print("Loading video, please wait...")
    sdp_str = requests.get("http://" + server_ip + ":" + str(port) + "/get-sdp?video-name=" + video + "&ip-address=" + server_ip).text

    sdp_loc = "client-temp\\" + video + ".sdp"
    sdp_file = open(sdp_loc, "w")
    sdp_file.write(sdp_str)
    play_video(sdp_loc)


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


