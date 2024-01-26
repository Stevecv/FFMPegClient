from flask import Flask
from waitress import serve
from flask import request

from client import setup_client
from server import setup_server

app = Flask(__name__)


def main_menu():
    print("""What is this computer working as
1. Server (Sender)
2. Client (Receiver)

-----------------------------------""")

    client_type = input("> ")

    if client_type == "1":
        setup_server()
    elif client_type == "2":
        setup_client()
    else:
        main_menu()


main_menu()


#@app.route("/play-video")
#def hello_world():
#    video = request.args.get("video")
#    print("Recieved request for video " + video)
#    return "Play video " + video
#
#
#serve(app, host='0.0.0.0', port=5000, threads=1)
