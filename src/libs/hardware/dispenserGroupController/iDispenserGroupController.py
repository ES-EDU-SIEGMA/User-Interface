from __future__ import annotations

import abc


class IDispenserGroupController(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass):
        return (
            hasattr(__subclass, "send_timings")
            and callable(__subclass.send_timings)
            and hasattr(__subclass, "get_identifier")
            and callable(__subclass.get_identifier)
            or NotImplemented,
        )

    @abc.abstractmethod
    def send_timings(self, timings: list[int]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_identifier(self) -> str:
        raise NotImplementedError
