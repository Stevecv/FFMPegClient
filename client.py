import requests


server_ip = ""


def get_sdp(video):
    print("get video sdp")


def video_chose_menu():
    video_list = requests.get("http://" + server_ip + ":5000/get-videos").text.split(",")

    i = 0
    for video in video_list:
        print(video_list[i])

        i += 1

    print("Enter a video number")
    print("-----------------------------------")
    video = input("> ")
    get_sdp(video)


def setup_client():
    global server_ip
    print("""What is the servers ip?

-----------------------------------""")
    server_ip = input("> ")

    video_chose_menu()


