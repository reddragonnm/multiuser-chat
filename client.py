import socket
import threading
import sys

from chatui import init_windows, read_command, print_message, end_windows
from json_handling import encode_packet, get_next_packet


def usage():
    print("usage: python client.py username address port")


def print_messages(sock):
    buffer = b""

    while True:
        buffer += sock.recv(10)
        next_packet = get_next_packet(buffer)

        if next_packet:
            payload, new_buffer = next_packet
            buffer = new_buffer

            if payload["type"] == "join":
                print_message(f"** {payload["username"]} joins!")
            elif payload["type"] == "chat":
                print_message(f"{payload["username"]}: {payload["message"]}")


def main(username, address, port):
    init_windows()

    s = socket.socket()
    s.connect((address, port))

    s.sendall(encode_packet({"type": "join", "username": username}))

    chat_thread = threading.Thread(target=print_messages, args=(s,))
    chat_thread.start()

    while True:
        message = read_command()

        if message == "/q":
            s.sendall(encode_packet({"type": "leave"}))
            break

        s.sendall(encode_packet({"type": "chat", "message": message}))

    chat_thread.join()
    s.close()
    end_windows()


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        address = sys.argv[2]
        port = int(sys.argv[3])
    except:
        usage()
        sys.exit(1)

    main(username, address, port)
