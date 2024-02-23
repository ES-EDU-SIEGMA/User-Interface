from __future__ import annotations

import abc


class IState(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass):
        return (
            hasattr(__subclass, "get_descriptor")
            and callable(__subclass.get_descriptor)
            and hasattr(__subclass, "run")
            and callable(__subclass.run)
            or NotImplemented()
        )

    @abc.abstractmethod
    def get_descriptor(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError()
