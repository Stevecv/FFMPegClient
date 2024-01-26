from client import setup_client
from server import setup_server

PORT = 5001


def main_menu():
    print("""What is this computer working as
1. Server (Sender)
2. Client (Receiver)

-----------------------------------""")

    client_type = input("> ")

    if client_type == "1":
        setup_server(PORT)
    elif client_type == "2":
        setup_client(PORT)
    else:
        main_menu()


main_menu()