import socket
import threading
import json
import sys

from chatui import init_windows, read_command, print_message, end_windows


def usage():
    print("usage: python client.py username address port")


def print_messages():
    pass


def main(username, address, port):
    init_windows()

    s = socket.socket()
    s.connect((address, port))

    chat_thread = threading.Thread(target=print_messages)
    chat_thread.start()

    while True:
        s = read_command()

        if s == "/q":
            break

        print_message(f"Me: {s}")

    chat_thread.join()
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
