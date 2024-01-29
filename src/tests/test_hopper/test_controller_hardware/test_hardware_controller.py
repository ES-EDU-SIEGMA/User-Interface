from __future__ import annotations
import unittest
from serial import Serial
from unittest.mock import MagicMock, Mock

from libs.hardware.controller.idispenser_array_controller import (
    IDispenserArrayController,
)
from libs.hardware.controller.dispenser_array_controller import (
    DispenserArrayController,
    PicoException,
)


class TestHopper(unittest.TestCase):
    __controller: IDispenserArrayController = None
    __serial: Serial = None
    __serial_readline_counter: int = 0

    def serial_readline_authenticate(self):
        self.__serial_readline_counter += 1
        if self.__serial_readline_counter == 1:
            return b"TEST_CON1\n"
        elif self.__serial_readline_counter == 2:
            return b"CALIBRATED\n"
        else:
            return b"F\n"

    def setUp(self):
        self.__serial = MagicMock()
        self.__serial.readline = Mock(side_effect=self.serial_readline_authenticate)

        self.__controller = DispenserArrayController(
            possible_identifiers=["TEST_CON1", "TEST_CON2"], port=self.__serial
        )

    def test_controller_initialized_failed(self):
        self.__serial.readline = Mock(return_value=b"F\n")
        self.assertRaises(
            PicoException,
            DispenserArrayController,
            possible_identifiers=[],
            port=self.__serial,
            max_connection_attempts=1,
        )

    def test_controller_is_initialized(self):
        self.assertIsNotNone(self.__controller)

    def test_controller_returns_correct_identifier(self):
        identifier: str = self.__controller.get_identifier()
        self.assertEqual(identifier, "TEST_CON1")

    def test_controller_send_correct_message(self):
        self.__serial.write = Mock()
        self.__controller.send_timings([10, 20, 30, 0])
        self.assertEqual(
            first=self.__serial.write.call_args.args[0], second=b"10;20;30;0\n"
        )


if __name__ == "__main__":
    unittest.main()
