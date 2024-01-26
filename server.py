import socket

def get_ip_address():
    try:
        # This will return the primary IP address associated with the machine
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except socket.error as e:
        print(f"Error: {e}")
        return None

def setup_server():
    print("Running server on " + get_ip_address())