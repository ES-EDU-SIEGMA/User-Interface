import unittest
from ..libs import json_data as JsonData


def test_correct_json_dict():
    json_drink_list = JsonData.get_drink_list()
    assert type(json_drink_list) is dict

    for drink_item in json_drink_list:
        assert type(drink_item) is dict
        assert type(drink_item["id"]) is int
        assert type(drink_item["name"]) is str
        assert type(drink_item["hopper"]) is int
        assert type(drink_item["dispensable"]) is bool
        assert type(drink_item["flow_speed"]) is int
        assert type(drink_item["mix_drink"]) is bool
        assert type(drink_item["requiredDrinks"]) is list[list[int]]
        drink_item.assertTrue(0 <= drink_item["hopper"] <= 11)


def test_get_drink_list():
    assert test_correct_json_dict()


# def test_write_dink_list():

# def test_get_drinks_on_hopper():

# def test_determine_dispensable_drinks():

# def test_add_drink():

# def change_drink_id_on_hopper():

# def test_reformat_json():

def test_create_beverage_drink_object(drink_id: int):
    # checks to confirm whether the created Beverage object confirms to the
    # information in the drink_list

    drink_list = JsonData.get_drink_list()
    beverage_object = JsonData.create_beverage_drink_object(drink_id)

    assert beverage_object.beverage_id == drink_id
    assert beverage_object.beverage_name == drink_list[str(drink_id)]["name"]
    assert beverage_object.beverage_hopper_id == drink_list[str(drink_id)]["hopper"]
    assert beverage_object.beverage_flow_speed == drink_list[str(drink_id)]["flow_speed"]


def test_create_mix_drink_object(drink_item: dict):
    # checks to confirm whether the created MixDrinkInformation object
    # confirms to the drink_item

    mix_drink_object = JsonData.create_mix_drink_object(drink_item)
    list_required_beverage_ids = list(list(zip(*drink_item["requiredDrinks"]))[0])

    assert mix_drink_object.mix_drink_id == drink_item["id"]
    assert mix_drink_object.mix_drink_name == drink_item["name"]
    assert mix_drink_object.mix_drink_needed_beverages == list_required_beverage_ids
    assert mix_drink_object.mix_drink_fill_perc_beverages == drink_item["requiredDrinks"]


# def test_get_all_other_beverages():

# def test_get_all_available_beverages():

# def test_change_beverage_on_hopper():

# def test_get_all_available_mix_drinks():

# def test_get_all_mixed_drinks():

# def test_is_name_available():

# def test_save_cocktails():

# def test_init():

# def test_close_connection():


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
