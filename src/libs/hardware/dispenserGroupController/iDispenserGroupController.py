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
            and hasattr(__subclass, "wait_for_ready_signal")
            and callable(__subclass.wait_for_ready_signal)
            or NotImplemented(),
        )

    @abc.abstractmethod
    def send_timings(self, timings: list[int]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_identifier(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def wait_for_ready_signal(self) -> None:
        raise NotImplementedError()
