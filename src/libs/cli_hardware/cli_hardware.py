import time


from libs.scale import scale_interface as scale_module


class CliHardware:
    __scale_object: scale_module.Scale
    __running: bool

    def __init__(self, __configuration_dict):
        self.__scale_object = scale_module.Scale(
            __configuration_dict["configure_mock_scale"],
            __configuration_dict["configure_measurement_calculation_method"],
            __configuration_dict["configure_measurements_per_scale_value"],
        )
        self.__running = True

        print("cmd: weight;<number-of-measurements>;<time-between>")
        self.__cli_hardware_loop()

    def __cli_hardware_loop(self):
        while self.__running:
            __input: list[str] = input().split(";")

            if __input[0] == "exit":
                self.__running = False

            elif __input[0] == "weight":
                if __input[1].isdigit() and __input[2].isdigit():
                    __current_number_measurements: int = 0
                    __max_number_measurements: int = int(__input[1])
                    __time_between_measurements_sec: int = int(__input[2])

                    while __current_number_measurements < __max_number_measurements:
                        __scale_value: int = self.__scale_object.get_weight()
                        print(f"value: {__scale_value}")
                        time.sleep(__time_between_measurements_sec)

                        __current_number_measurements += 1

                    print("cmd: weight;<number-of-measurements>;<time-between>")
                else:
                    print("wrong input;")
                    print("cmd: weight;<number-of-measurements>;<time-between>")
