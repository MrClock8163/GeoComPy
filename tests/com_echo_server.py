from os import environ

from serial import Serial


portname = environ.get("GEOCOMPY_TEST_PORT_SERVER", "")
if portname == "":
    raise ValueError(
        "Echo server serial port name must be set in "
        "'GEOCOMPY_TEST_PORT_SERVER' environment variable"
    )


def echo_server(port: str) -> None:
    com = Serial(port)
    try:
        com.reset_input_buffer()
        com.reset_output_buffer()
        while True:
            message = com.read()
            com.write(message)
    finally:
        com.close()


if __name__ == "__main__":
    echo_server(portname)
