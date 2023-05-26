def print_help_commands():
    print("input options: \n"
          "input <help>                           to see a list of available commands\n\n"
          "edit hopper cmds:\n"
          "input <beverages>                      to see a list of all beverages\n"
          "input <hoppers>                        to see a list of the current hopper layout\n"
          "input [<hopper-position>;<beverage>]   to put a beverage onto the hopper-position\n"
          "      example:  1;coca_cola\n\n"
          "change ui cmds:\n"
          "input <select>                         to dispense a drink\n"
          "input <new>                            to enter a new recipe\n"
          "input <exit>                           to exit the application")


class EditHopper:
    __data_hopper_names: list[str] = None
    __data_beverage_names: list[str] = None
    __commands: list[str] = ["drinks", "edit", "new", "exit"]
    __return_value: str = None
    __edit_hopper_process: bool = None

    def __init__(self):
        pass

    def activate(self, __data_hopper_names: list[str], __data_beverage_names: list[str]) -> str:
        self.__data_hopper_names = __data_hopper_names
        self.__data_beverage_names = __data_beverage_names
        self.__return_value = ""
        self.__edit_hopper_process = True

        print("you are currently in the edit-hopper window")
        print("enter <help> to see the available commands")
        return self.__edit_hopper_loop()

    def reactivate(self) -> str:
        self.__return_value = ""
        self.__edit_hopper_process = True
        print("enter <help> to see the available commands")
        return self.__edit_hopper_loop()

    def deactivate(self):
        pass

    def __edit_hopper_loop(self) -> str:
        while self.__edit_hopper_process:
            __input: str = input()
            self.__case_distinction(__input)
        return self.__return_value

    def __print_hopper_layout(self):
        print("the hopper layout:")
        __position: int = 0
        for __beverage in self.__data_hopper_names:
            print(f"hopper-position: {__position}   beverage: {__beverage}")
            __position += 1

    def __print_beverages(self):
        print("all beverages:")
        for __beverage in self.__data_beverage_names:
            print(__beverage)

    def __try_change_hopper(self, __input: str):
        # we are expecting a string input of two values separated by a ";"
        # the first of the two values should be an int in string format

        try:  # try to split the input
            __split_input = __input.split(";")
            if len(__split_input) == 2:  # the input should consist of exactly two values
                try:  # try to cast the first value into an integer
                    __hopper_position: int = int(__split_input[0])
                    __beverage: str = __split_input[1]  # this code isn't reached if the int cast fails
                    if __beverage in self.__data_beverage_names:  # check if we got a valid beverage name
                        self.__return_value = f"command;edit;{__hopper_position};{__beverage}"
                        self.__edit_hopper_process = False
                        print("hopper layout changed to:\n"
                              f"hopper-position: {__hopper_position}   beverage: {__beverage}")
                except ValueError:
                    print("please enter a valid hopper-position as an integer")
        except ValueError:
            pass

    def __case_distinction(self, __input: str) -> str:
        match __input:
            case "help":
                print_help_commands()
            case "beverages":
                self.__print_beverages()
            case "hoppers":
                self.__print_hopper_layout()
            case "select":
                self.__return_value = "change_window;select"
                self.__edit_hopper_process = False
            case "new":
                self.__return_value = "change_window;new"
                self.__edit_hopper_process = False
            case "exit":
                self.__return_value = "exit;pseudo_string"
                self.__edit_hopper_process = False
            case _:
                if self.__try_change_hopper(__input):
                    pass
                else:
                    print("please enter a valid input")
