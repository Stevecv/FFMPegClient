import requests

server_ip = ""


def get_sdp(video, port):
    sdp_str = requests.get("http://" + server_ip + ":" + port + "/get-sdp?video-name=" + video + "&ip-address=" + server_ip).text


def video_chose_menu(port):
    video_list = requests.get("http://" + server_ip + ":" + port + "/get-videos").text.split(",")

    i = 0
    for video in video_list:
        print(i + ". " + video_list[i])

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


