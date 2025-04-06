import socket
import select
import sys

from json_handling import encode_packet, get_next_packet


def usage():
    print("usage: python server.py port")


def print_logs(payload, username):
    print(payload if payload["type"] == "join" else {**payload, "username": username})


def main(port):
    s = socket.socket()
    s.bind(("0.0.0.0", port))
    s.listen()

    socks = {s}
    sock_data = dict()

    while True:
        available = select.select(socks, {}, {})[0]

        for sock in available:
            left = False

            if sock is s:
                new_sock, addr = s.accept()
                socks.add(new_sock)

                sock_data[new_sock] = {"username": "", "buffer": b""}
            else:
                data = sock.recv(2)
                sock_data[sock]["buffer"] += data

                new_packet = get_next_packet(sock_data[sock]["buffer"])
                if new_packet:
                    payload, new_buffer = new_packet
                    sock_data[sock]["buffer"] = new_buffer

                    print_logs(payload, sock_data[sock]["username"])

                    if payload["type"] == "join":
                        sock_data[sock]["username"] = payload["username"]

                        for all_sock in sock_data.keys():
                            if sock is not all_sock:
                                all_sock.sendall(encode_packet(payload))

                    elif payload["type"] == "chat":
                        for all_sock in sock_data.keys():
                            all_sock.sendall(
                                encode_packet(
                                    {**payload, "username": sock_data[sock]["username"]}
                                )
                            )

                    elif payload["type"] == "leave":
                        left = True
                        for all_sock in sock_data.keys():
                            if sock is not all_sock:
                                all_sock.sendall(
                                    encode_packet(
                                        {
                                            **payload,
                                            "username": sock_data[sock]["username"],
                                        }
                                    )
                                )

                if len(data) == 0 or left:
                    socks.remove(sock)
                    sock.close()
                    del sock_data[sock]


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
        print(f"Server listening on port {port}")
    except:
        usage()
        sys.exit(1)

    main(port)
