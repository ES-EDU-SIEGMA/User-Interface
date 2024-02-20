from __future__ import annotations
import abc


class IUserInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass):
        return (
            hasattr(__subclass, "display")
            and callable(__subclass.display)
            or NotImplemented
        )

    @abc.abstractmethod
    def display(self, input_data: list[str]) -> int:
        raise NotImplementedError()
