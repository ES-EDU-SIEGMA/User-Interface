def print_help_commands():
    print("input options: \n"
          "input <help>       to see a list of commands\n\n"
          "drink selection cmds:\n"
          "input <drinks>     to see a list of all available drinks\n"
          "input <drink-name> to dispense the drink\n\n"
          "change ui cmds:\n"
          "input <edit>       to edit the hopper layout\n"
          "input <new>        to enter a new recipe\n"
          "input <exit>       to exit the drink  selection")


class Selection:
    __data_drink_names: list[str] = None
    __commands: list[str] = ["help", "drinks", "edit", "new", "exit"]
    __return_value: str = None
    __drink_selection_process: bool = None

    def __init__(self):
        pass

    def activate(self, __data_drink_names: list[str]) -> str:
        self.__data_drink_names = __data_drink_names
        self.__return_value = ""
        self.__drink_selection_process = True

        print("enter <help> to see the available commands")
        return self.__drink_selection_loop()

    def reactivate(self) -> str:
        self.__return_value = ""
        self.__drink_selection_process = True

        print("enter <help> to see the available commands")
        return self.__drink_selection_loop()

    def deactivate(self):
        pass

    def __drink_selection_loop(self) -> str:
        while self.__drink_selection_process:
            __input: str = input()
            self.__case_distinction(__input)
        return self.__return_value

    def __print_drink_names(self):
        print("the following drinks are available:")
        for __drink_name in self.__data_drink_names:
            print(__drink_name)

    def __case_distinction(self, __input: str):
        if (__input in self.__data_drink_names) and (__input not in self.__commands):
            # the test "__input not in self.__commands" isn't necessary if we assume that drinks don't have a cmd name
            self.__return_value = f"command;selection;{__input}"
            self.__drink_selection_process = False
            print("your drink is being dispensed")

        else:
            match __input:
                case "help":
                    pass
                case "drinks":
                    self.__print_drink_names()
                case "edit":
                    self.__return_value = "change_window;edit"
                    self.__drink_selection_process = False
                case "new":
                    self.__return_value = "change_window;new"
                    self.__drink_selection_process = False
                case "exit":
                    self.__return_value = "exit;exit"
                    self.__drink_selection_process = False
                case _:
                    print("please enter a valid input")
