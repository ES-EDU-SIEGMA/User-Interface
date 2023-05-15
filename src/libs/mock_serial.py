"""

This class is to simulate the communication with the picos

"""

STANDARD_BAUDRATE = 115200  # hide type
buffer = None


def __init__():
    global buffer
    # self.port = port
    # self.baudrate = baudrate
    # self.responses = {
    # "LEFT": b"LEFT\r\n",
    # "RIGHT": b"RIGHT\r\n",
    # "RONDELL": b"RONDELL\r\n",
    # "CALIBRATED": b"CALIBRATED\r\n"
    # }

    # use list as queue to simulate serial byte transfer
    buffer = []


def readline(self) -> bytes:
    if self.buffer:
        return self.buffer.pop(0)
    else:
        return b''


"""
Picos are identified by the device they control.
Then calibrated comes in the queue
so that waitUntilReady() is properly simulated.
Failure case neglected. We create three objects
and have three picos for now.
"""


def write(self, input_data: str) -> None:
    if input_data == b'i\n':
        if "LEFT" in self.port:
            self.buffer.append(self.responses["LEFT", "CALIBRATED"])
            print("left pico calibrated")
        elif "RIGHT" in self.port:
            self.buffer.append(self.responses["RIGHT", "CALIBRATED"])
            print("right pico calibrated")
        elif "RONDELL" in self.port:
            self.buffer.append(self.responses["RONDELL", "CALIBRATED"])
            print("rondell calibrated")


def send_msg(pico_id: int, input_msg: str):
    pass


def close_connection() -> None:
    pass
