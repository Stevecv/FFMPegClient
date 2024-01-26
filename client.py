import requests


server_ip = ""


def video_chose_menu():
    video_list = requests.get("http://" + server_ip + ":5000/get-videos")
    print(video_list.text)


def setup_client():
    global server_ip
    print("""What is the servers ip?

-----------------------------------""")
    server_ip = input("> ")

    video_chose_menu()


