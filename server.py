import socket
import select
import json
import sys


def usage():
    print("usage: python server.py port")


def main(port):
    s = socket.socket()
    s.bind(("localhost", port))
    s.listen()

    socks = {s}

    while True:
        available = select.select(socks, {}, {})[0]

        for sock in available:
            if sock is s:
                new_sock, addr = s.accept()
                socks.add(new_sock)

                print(addr)
            else:
                data = sock.recv(4096)
                print(data)

                if len(data) == 0:
                    socks.remove(sock)


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
        print(f"Server listening on port {port}")
    except:
        usage()
        sys.exit(1)

    main(port)
