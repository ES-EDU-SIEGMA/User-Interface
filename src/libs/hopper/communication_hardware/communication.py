import serial
import time


class Communication:
    """ hopper-positions:
            <left-pico>:= hopper-positions 0-3
            <right-pico>:= hopper-positions 4-7
            <rondell-pico>:= hopper-positions 8-11

        __hopper_configuration:= {<response-signal>: [<hopper-size-ml>]}
            <response-signal>:= "LEFT" | "RIGHT" | "RONDELL

        STANDARD_BAUDRATE:= constant that is used for initializing serial communication-objects
        __picos_hardware:= __picos_hardware:= [<serial-object-left>, <serial-object-right>, <serial-object-rondell>]
        __hopper_sizes:= [<hopper-size-ml>] where the hopper position is encoded into the list position"""

    STANDARD_BAUDRATE = 115200

    __picos_hardware: list[serial.Serial]
    __hopper_sizes: list[int]

    def __init__(self, __hopper_sizes: list[int]):

        self.__hopper_sizes = __hopper_sizes

        try:
            self.__picos_hardware = [serial.Serial("/dev/ttyACM0", self.STANDARD_BAUDRATE),
                                     serial.Serial("/dev/ttyACM1", self.STANDARD_BAUDRATE),
                                     serial.Serial("/dev/ttyACM2", self.STANDARD_BAUDRATE)]
        except Exception as error:
            print(error)
            raise Exception("error while establishing a serial connection")

        self.__identify_picos()
        self.__wait_until_ready()
        # todo think about how long we want to wait in __wait_until_ready() currently there is no limit.

    def __identify_picos(self):
        """ Get each pico to send a signal [__signal in [b"LEFT\r\n", b"RIGHT\r\n", b"RONDELL\r\n"]] to identify
            what serial-object connects th which hoppers.
            Changes the __picos_hardware <serial-object> positioning so that:
                __picos_hardware[0]==<serial-object-left>
                __picos_hardware[1]==<serial-object-right>
                __picos_hardware[2]==<serial-object-rondell>"""

        __temp_picos_hardware: list[serial.Serial] = [None, None, None]
        __picos_identified: int = 0

        for __pico_connection in self.__picos_hardware:
            __current_identification_attempt = 0
            __max_attempts = 5
            # __max_attempts is chosen arbitrarily

            while __current_identification_attempt < __max_attempts:
                self.__write_pico(__pico_connection, bytes("i\n", "utf-8"))
                # write the signal "i\n" to the pico, to get a response signal for the hopper identification
                __pico_response: bin = self.__read_pico(__pico_connection)
                # __pico_response is currently b"LEFT\r\n"  |  b"RIGHT\r\n"  |  b"RONDELL\r\n"  |  b"F\r\n"

                match __pico_response:
                    case b'LEFT\r\n':
                        __temp_picos_hardware[0] = __pico_connection
                        __picos_identified += 1
                    case b'RIGHT\r\n':
                        __temp_picos_hardware[1] = __pico_connection
                        __picos_identified += 1
                    case b'RONDELL\r\n':
                        __temp_picos_hardware[2] = __pico_connection
                        __picos_identified += 1
                    case b'F\r\n':
                        # a communication error occurred
                        __current_identification_attempt += 1
                        time.sleep(5)

        self.__picos_hardware = __temp_picos_hardware

        if None in __temp_picos_hardware:
            # check if all picos are identified and throw an exception if we weren't able to identify all picos
            # todo optionally: add error handling to make a new attempt in identifying the picos
            raise Exception("Not all picos were able to establish a connection")

    def __wait_until_ready(self):
        __ready_picos: int = 0
        while __ready_picos < len(self.__picos_hardware):
            for __pico_connection in self.__picos_hardware:
                __pico_response: bin = self.__read_pico(__pico_connection)
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
                # We don't rly need an exception here as this error only occurs if the connection is already lost.
                # todo remove raise Exception or maybe add some error handling
                raise Exception("error while closing pico connections")

    def send_timings(self, __timings: list[int]):
        pass

    ####################################################################################################################
    # f"{hopperTimings[0]};{hopperTimings[1]};{hopperTimings[2]};{hopperTimings[3]};\n"
    ####################################################################################################################

    @staticmethod
    def __send_msg(__pico_connection: serial.Serial, __timings):
        # send the input to the pico with the correct id

        # todo change this
        try:
            __pico_connection.write(bytes(__timings, "utf-8"))
        except Exception as error:
            raise error

    @staticmethod
    def __write_pico(__pico_connection: serial.Serial, __input):
        """ this method is used to write to picos and offer error handling"""
        # todo add error handling
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