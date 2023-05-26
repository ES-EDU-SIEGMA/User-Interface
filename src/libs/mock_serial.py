"""

This class is to simulate the communication with the picos

"""

STANDARD_BAUDRATE = 115200


class Serial:
    PORT: str
    BAUDRATE: int
    RESPONSES: dict[str, str] = {
        "LEFT": b"LEFT\n",
        "RIGHT": b"RIGHT\n",
        "RONDELL": b"RONDELL\n",
        "CALIBRATED": b"CALIBRATED\n",
    }
    RESPONSE_BUFFER: [str]

    def __init__(self, port: str, baudrate: int):
        self.PORT = port
        self.BAUDRATE = baudrate
        self.RESPONSE_BUFFER = []

    def readline(self) -> bytes:
        if self.RESPONSE_BUFFER:
            return self.RESPONSE_BUFFER.pop(0)
        else:
            return b""

    """
    Picos are identified by the device they control.
    Then calibrated comes in the queue
    so that waitUnitlReady() is properly simulated.
    Failure case neglected. We create three objects
    and have three picos for now.
    """

    def write(self, input_data) -> None:
        if input_data == b"i\n":
            if "/dev/ttyACM0" in self.PORT:
                self.RESPONSE_BUFFER.append(self.RESPONSES["LEFT"])
                self.RESPONSE_BUFFER.append(self.RESPONSES["CALIBRATED"])
            elif "/dev/ttyACM1" in self.PORT:
                self.RESPONSE_BUFFER.append(self.RESPONSES["RIGHT"])
                self.RESPONSE_BUFFER.append(self.RESPONSES["CALIBRATED"])
            elif "/dev/ttyACM2" in self.PORT:
                self.RESPONSE_BUFFER.append(self.RESPONSES["RONDELL"])
                self.RESPONSE_BUFFER.append(self.RESPONSES["CALIBRATED"])

    def close(self) -> None:
        pass
