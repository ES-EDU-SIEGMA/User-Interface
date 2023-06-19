__picos_hardware = [1, 2]


def __create_hopper_messages(__timings: list[list[int]]) -> list[list[str]]:
    # __timings: [[<hopper_emptying_count>, <time_per_emptying>]]
    # return list[list[<hopper-timing-msg>]]

    __messages_all_hoppers: list[list[str]] = []

    for __serial_index in range(len(__picos_hardware)):
        # print(f"serial_index: {__serial_index}\n")
        __messages_pico: list[str] = []

        while (
                __timings[__serial_index * 4 + 0][0]
                or __timings[__serial_index * 4 + 1][0]
                or __timings[__serial_index * 4 + 2][0]
                or __timings[__serial_index * 4 + 3][0]
        ):
            # check if <hopper_emptying_count> is not 0 for one of the 4 hoppers that connect to a Tiny

            __one_message_to_pico: str = ""
            # print(f"one_message_to_pico: {__one_message_to_pico}")
            # __one_message_to_pico = "<timing-1>;<timing-2>;<timing-3>;<timing-4>;\n

            for __hopper_index in range(4):
                __index: int = __serial_index * 4 + __hopper_index

                if __timings[__index][0]:
                    # check if <hopper_emptying_count> > 0
                    __one_message_to_pico += f"{__timings[__index][1]};"
                    __timings[__index][0] -= 1
                    # print(f"none 0: {__one_message_to_pico}")
                else:
                    # <hopper_emptying_count> is 0
                    __one_message_to_pico += "0;"
                    # print(f"is 0: {__one_message_to_pico}")

            __messages_pico.append(f"{__one_message_to_pico}\n")
            # print(f"one_message_pico: {__one_message_to_pico}")
            # print(f"messages_pico: {__messages_pico}")

        if __messages_pico:
            __messages_all_hoppers.append(__messages_pico)
            # print(f"messages_all_hoppers: {__messages_all_hoppers}\n")

    print(f"timings result: {__messages_all_hoppers}")
    return __messages_all_hoppers


timings = [[2, 1000], [3, 1000], [0, 0], [1, 1000],
           [1, 500], [4, 500], [0, 500], [2, 500]]


# send_timings(timings)


def send_timings(__timings: list[list[int]]):
    # __timings: [[<hopper_emptying_count>, <time_per_emptying>]] list-position = hopper-position

    __hopper_messages: list[list[str]] = __create_hopper_messages(__timings)
    # __hopper_messages: list[list[str]] = [<hopper-messages-tiny>]
    # <hopper-messages-tiny>: list[str] = [<hopper-message>]

    for __tiny_pico_index in range(len(__picos_hardware)):
        print("iteration")
        while __hopper_messages[__tiny_pico_index]:
            # check if there is a message to send for a tiny pico
            __msg_to_send: str = __hopper_messages[__tiny_pico_index].pop(0)
            # self.__send_msg(self.__picos_hardware[__tiny_pico_index], __msg_to_send)
            # print(f"sending msg: {__msg_to_send}")
            print(bytes(__msg_to_send, "utf-8"))


send_timings(timings)
