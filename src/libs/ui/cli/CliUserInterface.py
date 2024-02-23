from __future__ import annotations

from libs.ui.IUserInterface import IUserInterface


class CliUserInterface(IUserInterface):
    __pre_message: str = """
If you want to abort please enter 0 and confirm with enter.
Please choose a option by entering the number and confirm with enter:
"""
    __post_message: str = """
Selection:  """

    def display_list_and_wait_for_user_selection(self, input_data: list[str]) -> int:
        """
        :param input_data: list of strings to be displayed
        :return: -1 for abort else index of item in input_data

        **IMPORTANT** -> List indexing starts with 0!
        """
        while True:
            print(self.__pre_message)
            for index, value in enumerate(input_data):
                print(f"  {index + 1}: {value}")
            user_selection = input(self.__post_message)
            if self.__user_input_valid(
                user_input=user_selection, max_id=len(input_data)
            ):
                return int(user_selection) - 1
            else:
                print("Your input was invalid. Please try again.")

    @staticmethod
    def __user_input_valid(user_input: str, max_id: int) -> bool:
        if not user_input.isnumeric():
            return False
        if max_id < int(user_input):
            return False
        return True

    def display_message_and_wait_for_user_response(self, input_data: str) -> None:
        print(input_data)
        input("Please press any key to continue!")

    def display_status(self, input_data: str) -> None:
        print(input_data)
