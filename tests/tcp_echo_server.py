from os import environ

import socket


portname = environ.get("GEOCOMPY_TEST_TCPPORT_SERVER", "")
if portname == "":
    raise ValueError(
        "Echo server serial port name must be set in "
        "'GEOCOMPY_TEST_TCPPORT_SERVER' environment variable"
    )


def echo_server(port: int) -> None:
    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_TCP
    ) as soc:
        soc.bind(("127.0.0.1", port))
        while True:
            soc.listen(1)
            print(f"Listening on {port}")
            server, address = soc.accept()
            print(f"Connected to {address}")

            with server:
                while True:
                    try:
                        data = server.recv(1024)
                        if data == b"":
                            break

                        data = data.strip(b"\r\n")
                        if data != b"":
                            server.send(data + b"\r\n")

                    except Exception:
                        break


if __name__ == "__main__":
    echo_server(int(portname))
