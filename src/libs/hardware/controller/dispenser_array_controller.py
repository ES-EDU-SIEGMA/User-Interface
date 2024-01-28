from __future__ import annotations
from serial import Serial
from serial.serialutil import SerialException
from time import sleep

from libs.hardware.controller.idispenser_array_controller import (
    IDispenserArrayController,
)


class PicoException(Exception):
    pass


class DispenserArrayController(IDispenserArrayController):
    __pico_port: Serial = None
    __max_connection_attempts: int = None
    __identifier: str = None

    def __init__(
        self,
        possible_identifiers: list[str],
        port: Serial,
        max_connection_attempts: int = 5,
    ):
        """
        :param possible_identifiers: list of available identifiers to validate against
        :param port: name of the serial port to use
        :param baudrate: baudrate for the serial port
        :param max_connection_attempts: attempts to connect before giving up
        """
        self.__pico_port = port
        self.__max_connection_attempts = max_connection_attempts

        self.__identify_controller(valid_identifiers=possible_identifiers)
        self.__wait_for_ready_signal()

    def send_timings(self, timings: list[int]) -> None:
        """
        :param timings: list of timings to send to the controller
        :return:
        """
        try:
            msg: str = ";".join(map(str, timings))
            self.__write(message=msg)
        except SerialException:
            raise PicoException("Send Timing Failed!")

    def get_identifier(self) -> str:
        """
        :return: The identifier received from the controller
        """
        return self.__identifier

    def __identify_controller(self, valid_identifiers: list[str]) -> None:
        try:
            self.__pico_port.reset_input_buffer()
            self.__pico_port.reset_output_buffer()
            for attempt in range(1, self.__max_connection_attempts):
                self.__write(message="i")
                response = self.__read()
                if response in valid_identifiers:
                    self.__identifier = response
                    break
                sleep(5.0)
            else:
                raise PicoException("Max Attempts reached!")
        except ConnectionRefusedError:
            raise PicoException("Connection Refused!")

    def __wait_for_ready_signal(self):
        while True:
            response = self.__read()
            if response.__eq__("CALIBRATED"):
                break

    def __read(self) -> str:
        return self.__pico_port.readline().decode("utf-8").rstrip()

    def __write(self, message: str) -> None:
        self.__pico_port.write(f"{message}\n".encode("utf-8"))
