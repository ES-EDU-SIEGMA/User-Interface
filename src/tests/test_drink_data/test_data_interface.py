from libs.drink_data import data_interface as Data_interface_module
import unittest


class MyTestCase(unittest.TestCase):

    __data_object: Data_interface_module.DataInterface

    __hopper_position_and_amount = {
            "Test_ingredient1": {"hopper_position": 0, "amount": 500},
            "Test_ingredient2": {"hopper_position": 1, "amount": 500},
            "Test_ingredient3": {"hopper_position": 2, "amount": 500},
            "Test_ingredient4": {"hopper_position": 3, "amount": 500},
            "Test_ingredient5": {"hopper_position": 4, "amount": 500},
            "Test_ingredient6": {"hopper_position": 5, "amount": 500},
            "Test_ingredient7": {"hopper_position": 6, "amount": 500},
            "Test_ingredient8": {"hopper_position": 7, "amount": 500},
            "Test_ingredient9": {"hopper_position": 8, "amount": 500},
            "Test_ingredient10": {"hopper_position": 9, "amount": 500},
            "Test_ingredient11": {"hopper_position": 10, "amount": 500},
            "Test_ingredient12": {"hopper_position": 11, "amount": 500}
    }

    def __create_data_object(self):
        self.__data_object = Data_interface_module.DataInterface(__hopper_position_and_amount)

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
