from __future__ import annotations

import abc


class IUserInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass):
        return (
            hasattr(__subclass, "display_list_and_wait_for_user_selection")
            and callable(__subclass.display_list_and_wait_for_user_selection)
            and hasattr(__subclass, "display_message_and_wait_for_user_response")
            and callable(__subclass.display_message_and_wait_for_user_response)
            and hasattr(__subclass, "display_status")
            and callable(__subclass.displays_status)
            or NotImplemented
        )

    @abc.abstractmethod
    def display_list_and_wait_for_user_selection(self, input_data: list[str]) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def display_message_and_wait_for_user_response(self, input_data: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def display_status(self, input_data: str) -> None:
        raise NotImplementedError()
