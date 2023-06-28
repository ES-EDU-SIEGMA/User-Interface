from libs.hopper.timing_calculation import (
    timing_calculation as timing_calculation_module,
)


class Hopper:
    __calculation_object: timing_calculation_module.Calculation

    __expected_weight: int

    def __init__(
        self,
        __mock_communication: bool,
        __ms_per_ml: int,
        __hopper_sizes: list[int],
        __pico_identifier: list[str],
        __serial_connections: list[str],
        __max_serial_identifier_attempt: int,
    ):
        if __mock_communication:
            # check if communication should be mocked
            from libs.hopper.communication_hardware import (
                mock_communication as mock_communication_module,
            )

            self.__communication_object = mock_communication_module.Communication()

        else:
            # normal communication with the hopper
            from libs.hopper.communication_hardware import (
                communication as communication_module,
            )

            self.__communication_object = communication_module.Communication(
                __pico_identifier, __serial_connections, __max_serial_identifier_attempt
            )

        self.__calculation_object = timing_calculation_module.Calculation(
            __ms_per_ml, __hopper_sizes
        )
        self.__expected_weight = 0

    def dispense_drink(self, __data: dict):
        __tmp: dict = self.__calculation_object.calculate_timing(__data)
        self.__expected_weight: int = __tmp["expected_weight"]

        self.__communication_object.send_timings(__tmp["timings"])

    def get_expected_weight(self) -> int:
        return self.__expected_weight

    def close(self):
        self.__communication_object.close_connection()
