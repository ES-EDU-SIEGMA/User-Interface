import serial
import time


class Communication:
    """
    __configure_tiny:= {<tiny-identifier>: [{hopper_position: <hopper-position>}]}

    STANDARD_BAUDRATE:= constant that is used for initializing serial communication-objects
    __picos_hardware:= [<serial-object>]
    __pico_hopper_mapping:= [[<hopper-position>]]
    """

    STANDARD_BAUDRATE = 115200

    __picos_hardware: list[serial.Serial]

    def __init__(self, __pico_identifier: list[str], __serial_connections: list[str],
                 __max_serial_identifier_attempt: int):

        try:
            for __serial_connection in __serial_connections:
                self.__picos_hardware.append(serial.Serial(__serial_connection, self.STANDARD_BAUDRATE))
        except Exception:
            raise Exception("error: error while establishing connections to the tinys.")

        self.__identify_picos(__pico_identifier, __max_serial_identifier_attempt)
        self.__wait_until_ready()
        # todo: think about how long we want to wait in __wait_until_ready() currently there is no limit.

    def __identify_picos(self, __pico_identifier: list[str], __max_serial_identifier_attempt: int):
        """ Get each pico to send a hopper-identifier signal to identify what serial uses which hopper.
            Changes the __picos_hardware <serial-object> positioning so that:
                __picos_hardware[0]==<serial-object-identifier-1>
                __picos_hardware[1]==<serial-object-identifier-2>
                __picos_hardware[2]==<serial-object-identifier-3>
                ...
                """

        __temp_picos_hardware: list[serial.Serial | None] = [None] * len(__pico_identifier)

        __pico_identifier_responses: list[bytes] = self.__get_pico_identifier_byte_conversion(__pico_identifier)

        for __pico_connection in self.__picos_hardware:

            __current_identification_attempt = 0

            while __current_identification_attempt < __max_serial_identifier_attempt:
                # limit the number of identification attempts for each serial connection

                self.__write_pico(__pico_connection, bytes("i\n", "utf-8"))
                # write the signal "i\n" to the pico, to get a response signal for the hopper identification
                __pico_response: bytes = self.__read_pico(__pico_connection)

                if __pico_response in __pico_identifier_responses:
                    # check if we received a known pico identifier

                    __index = __pico_identifier_responses.index(__pico_response)

                    if __pico_response == b'F\r\n':
                        # check if an error occurred during data transmission
                        __current_identification_attempt += 1
                        time.sleep(5)

                    elif __temp_picos_hardware[__index] is None:
                        # check if this pico identifier isn't already used
                        __temp_picos_hardware[__index] = __pico_connection

                    else:
                        raise Exception("error: two tinys send the same connection identifier")

                else:
                    raise Exception("error: received an unknown pico identifier")

        self.__picos_hardware = __temp_picos_hardware

        if None in __temp_picos_hardware:
            # check if all picos are identified and throw an exception if we weren't able to identify all picos
            # todo optionally: add error handling to make a new attempt in identifying the picos
            raise Exception("Not all picos were able to establish a connection")

    @staticmethod
    def __get_pico_identifier_byte_conversion(__pico_identifier: list[str]) -> list[bytes]:
        # return pico identifiers as a byte list

        __result: list[bytes] = []

        for __pico_identifier in __pico_identifier:
            __pico_identifier = f"{__pico_identifier}\r\n"
            __result.append(bytes(__pico_identifier, "utf-8"))

        __result.append(b'F\r\n')

        return __result

    def __wait_until_ready(self):
        # wait until all picos send the calibrated signal.
        # todo: think about whether we should wait endlessly or change this
        __ready_picos: int = 0
        while __ready_picos < len(self.__picos_hardware):
            for __pico_connection in self.__picos_hardware:
                __pico_response: bytes = self.__read_pico(__pico_connection)
                if __pico_response == b"CALIBRATED\r\n":
                    __ready_picos += 1

    ####################################################################################################################
    # Methods that can be called by other objects
    ####################################################################################################################

    def close_connection(self):

        for __pico_connection in self.__picos_hardware:

            try:
                __pico_connection.close()
            except Exception:
                raise Exception("error while closing pico connections")

    def send_timings(self, __timings: list[list[int]]):
        # __timings: [[<hopper_emptying_count>, <time_per_emptying>]] list-position = hopper-position

        __hopper_messages: list[list[str]] = self.__create_hopper_messages(__timings)

        for __serial_index in range(len(self.__picos_hardware)):
            if __hopper_messages[__serial_index]:
                __msg_to_send: str = __hopper_messages[__serial_index].pop(0)
                self.__send_msg(self.__picos_hardware[__serial_index], __msg_to_send)

    ####################################################################################################################
    # Methods to create the messages for pico communication
    ####################################################################################################################

    def __create_hopper_messages(self, __timings: list[list[int]]) -> list[list[str]]:
        # __timings: [[<hopper_emptying_count>, <time_per_emptying>]]
        # return list[list[<hopper-timing-msg>]]]

        __messages_all_hoppers: list[list[str]] = []

        for __serial_index in range(len(self.__picos_hardware)):

            __messages_pico: list[str] = []

            while (__timings[__serial_index * 4 + 0][0] or
                   __timings[__serial_index * 4 + 1][0] or
                   __timings[__serial_index * 4 + 2][0] or
                   __timings[__serial_index * 4 + 3][0]):
                # check if hopper_emptying_count for one of the 4 hoppers is not 0.
                # meaning there is still liquid to be dispensed.

                __one_message_to_pico: str = ""

                for __hopper_index in range(4):
                    __index: int = __serial_index * 4 + __hopper_index

                    if __timings[__index][0]:
                        __one_message_to_pico += f"{__timings[__index]};"
                    else:
                        __one_message_to_pico += "0;"

                __messages_pico.append(f"{__one_message_to_pico}\n")

                if __messages_pico:
                    __messages_all_hoppers.append(__messages_pico)

            return __messages_all_hoppers

    ####################################################################################################################
    # Methods to communicate with the pico
    ####################################################################################################################

    @staticmethod
    def __send_msg(__pico_connection: serial.Serial, __timings):
        # send the input to the pico with the correct id

        try:
            __pico_connection.write(bytes(__timings, "utf-8"))
        except Exception as error:
            raise error

    @staticmethod
    def __write_pico(__pico_connection: serial.Serial, __input):
        """ this method is used to write to picos and offer error handling"""
        # todo add error handling
        # todo include this one in __send_msg by not encoding __input to byte format
        try:
            __pico_connection.write(__input)
        except Exception as error:
            print(error)
            raise Exception("Error during pico writing process")

    @staticmethod
    def __read_pico(__pico_connection: serial.Serial) -> bin:
        """ this method is used to read from picos and offer error handling"""
        # todo add error handling
        try:
            return __pico_connection.readline()
        except Exception as error:
            print(error)
            raise Exception("Error during pico reading process")
