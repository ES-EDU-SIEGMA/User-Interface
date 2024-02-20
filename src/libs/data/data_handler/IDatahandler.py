from __future__ import annotations
import abc

from libs.data.datatypes.drink import Drink
from libs.data.datatypes.ingredient import Ingredient


class IDatahandler(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass):
        return (
            hasattr(__subclass, "read_ingredients")
            and callable(__subclass.read_ingredients)
            and hasattr(__subclass, "write_ingredients")
            and callable(__subclass.write_ingredients)
            and hasattr(__subclass, "read_drinks")
            and callable(__subclass.read_drinks)
            and hasattr(__subclass, "write_drinks")
            and callable(__subclass.write_drinks)
            or NotImplemented
        )

    @abc.abstractmethod
    def read_ingredients(self) -> list[Ingredient]:
        raise NotImplementedError()

    @abc.abstractmethod
    def write_ingredients(self, ingredients: list[Ingredient]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def read_drinks(self) -> list[Drink]:
        raise NotImplementedError()

    @abc.abstractmethod
    def write_drinks(self, drinks: list[Drink]) -> None:
        raise NotImplementedError()
