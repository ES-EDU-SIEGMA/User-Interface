import unittest
from unittest.mock import MagicMock, Mock
from random import randint

from libs.hardware.scale.scale import Scale
from libs.hardware.tatobari_hx711.emulated_hx711 import HX711


class TestScale(unittest.TestCase):
    __scale: Scale = None
    __hx711: HX711 = None

    def setUp(self):
        self.__hx711 = MagicMock()
        self.__scale = Scale(hardware=self.__hx711)

    def test_initial_tare(self):
        self.__hx711.get_weight = Mock(return_value=0)
        self.assertEqual(0, self.__scale.get_weight())

    def test_tare_function(self):
        self.__hx711.get_weight = Mock(return_value=5)
        self.__scale.tare()
        self.assertEqual(0, self.__scale.get_weight())

    def test_get_weight_with_tare_equals_zero(self):
        returned_weight_from_mock = randint(0, 1000)
        self.__hx711.get_weight = Mock(return_value=returned_weight_from_mock)
        self.assertEqual(returned_weight_from_mock * 1000, self.__scale.get_weight())

    def test_get_weight_with_tare_unequal_zero(self):
        self.__hx711.get_weight = Mock(return_value=10)
        self.__scale.tare()
        returned_weight_from_mock = randint(0, 1000)
        self.__hx711.get_weight = Mock(return_value=returned_weight_from_mock)
        self.assertEqual(
            (returned_weight_from_mock - 10) * 1000, self.__scale.get_weight()
        )


if __name__ == "__main__":
    unittest.main()
