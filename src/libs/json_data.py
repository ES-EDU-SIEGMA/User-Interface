import json
from . import runtime_data as runtime_data

DRINKLIST_FILE_PATH: str = ""


def __init__(path_to_drinklist_file: str):
    global DRINKLIST_FILE_PATH
    DRINKLIST_FILE_PATH = path_to_drinklist_file


def get_drink_list() -> dict:
    global DRINKLIST_FILE_PATH
    """returns the drink_list file as a dict"""

    try:
        with open(file=DRINKLIST_FILE_PATH, mode="r") as jsonFile:
            data = json.load(jsonFile)
            return data

    except Exception as error:
        print(error)
        return {}


def write_drink_list(new_drink_list: dict):
    """writes the parameter of the function into the drink_list file"""
    global DRINKLIST_FILE_PATH

    try:
        with open(file=DRINKLIST_FILE_PATH, mode="w") as jsonFile:
            json.dump(new_drink_list, jsonFile, indent=4)

    except Exception as error:
        print(error)


def get_drinks_on_hopper() -> list[int]:
    """returns the IDs of all drinks on the hopper"""

    drink_list: dict = get_drink_list()
    result_hopper_ids: list[int] = []

    for drink_item in drink_list:
        if drink_list[drink_item]["hopper_id"] is not None:
            result_hopper_ids.append(drink_list[drink_item]["id"])

    return result_hopper_ids


def determine_dispensable_drinks():
    """Changes the dispensable value of a drink depending on whether a drink is
    dispensable. A drink is dispensable if all required drinks are on the hopper"""

    drink_list = get_drink_list()
    drink_ids_on_hopper = get_drinks_on_hopper()

    for drink_item in drink_list:
        drink_list[drink_item]["dispensable"] = False

        if drink_list[drink_item]["mix_drink"] is False:
            if drink_list[drink_item]["hopper_id"] is not None:
                drink_list[drink_item]["dispensable"] = True

        else:
            list_required_beverage_ids = list(
                list(zip(*drink_list[drink_item]["needed_beverages"]))[0]
            )
            # list_required_drink_id is a list of all required drinkIDs for a drink

            if all(
                drink_id in drink_ids_on_hopper
                for drink_id in list_required_beverage_ids
            ):
                # tests whether the list of required drinkIDs is a subset of the list of drinkIDs on the hopper
                drink_list[drink_item]["dispensable"] = True

    write_drink_list(drink_list)
    # updates the dispensable value for all drinks


def add_drink(
    mix_drink: bool,
    new_drink_id: int = None,
    name: str = None,
    required_drinks: [[int]] = None,
    flow_speed: int = None,
):
    """Adds a new drink to the drink_list and determines whether the drink can be dispensed"""

    if required_drinks is None:
        required_drinks = []
    drink_list = get_drink_list()
    drink_list[str(new_drink_id)] = {
        "id": new_drink_id,
        "name": name,
        "hopper_id": None,
        "dispensable": False,
        "flow_speed": flow_speed,
        "mix_drink": mix_drink,
        "needed_beverages": required_drinks,
    }

    write_drink_list(drink_list)
    determine_dispensable_drinks()


def change_drink_id_on_hopper(hopper_id: int, new_drink_on_hopper_id: int):
    """changes the hopper_id for the given drink_id to the parameter hopper_id and
    changes the hopper_id for the previous drink on the hopper to None and
    determines which drinks are dispensable"""

    drink_list: dict = get_drink_list()

    for drink_item in drink_list:
        if drink_list[drink_item]["hopper_id"] == hopper_id:
            drink_list[drink_item]["hopper_id"] = None
        # remove the old drink from the hopper by setting hopper_id to None

        if drink_list[drink_item]["id"] == new_drink_on_hopper_id:
            drink_list[drink_item]["hopper_id"] = hopper_id
        # update the hopper_id for the new drink

    write_drink_list(drink_list)
    determine_dispensable_drinks()


def get_highest_id() -> int:
    drink_list: dict = get_drink_list()
    highest_id: int = 0
    # assumes that the drink_list isn't empty

    for drink_id in drink_list:
        if drink_list[drink_id]["id"] > highest_id:
            highest_id = drink_list[drink_id]["id"]

    return highest_id


def reformat_json():
    """reformat the jsonfile after manually changing it for aesthetic purposes"""

    drinks = get_drink_list()
    write_drink_list(drinks)


# The following code implements the already existing Sql-code through Json
def create_beverage_drink_object(drink_id: int) -> runtime_data.Beverage:
    """creates a Beverage object from RuntimeData"""

    drink_list: dict = get_drink_list()
    beverage_hopper_id: int = drink_list[str(drink_id)]["hopper_id"]
    beverage_name: str = drink_list[str(drink_id)]["name"]
    beverage_flow_speed: int = drink_list[str(drink_id)]["flow_speed"]

    return runtime_data.Beverage(
        drink_id, beverage_hopper_id, beverage_name, beverage_flow_speed
    )


def create_mix_drink_object(drink_item: dict) -> runtime_data.MixDrinkInformation:
    """creates a mix_drink_Object from RuntimeData"""

    mix_drink_id: int = drink_item["id"]
    mix_drink_name: str = drink_item["name"]
    mix_drink_needed_beverages: list[runtime_data.Beverage] = []
    mix_drink_fill_perc_beverages: list[list[int]] = drink_item["needed_beverages"]

    for beverage_id in list(list(zip(*drink_item["needed_beverages"]))[0]):
        mix_drink_needed_beverages.append(create_beverage_drink_object(beverage_id))

    return runtime_data.MixDrinkInformation(
        mix_drink_id,
        mix_drink_name,
        mix_drink_fill_perc_beverages,
    )


def get_all_other_beverages() -> list[runtime_data.Beverage]:
    """returns a list of Beverage objects which are not on the hopper"""

    drink_list: dict = get_drink_list()
    beverages_not_on_hopper: list[runtime_data.Beverage] = []

    for drink_id in drink_list:
        if (drink_list[drink_id]["hopper_id"] is None) and (
            not drink_list[drink_id]["mix_drink"]
        ):
            beverages_not_on_hopper.append(create_beverage_drink_object(drink_id))

    return beverages_not_on_hopper


def get_all_available_beverages() -> list[runtime_data.Beverage]:
    """returns a list of Beverage objects which are active on the hopper"""

    drink_list: dict = get_drink_list()
    beverage_result: list[runtime_data.Beverage] = []

    for drink_id in drink_list:
        if (drink_list[drink_id]["hopper_id"] is not None) and (
            not drink_list[drink_id]["mix_drink"]
        ):
            beverage_result.append(create_beverage_drink_object(drink_id))

    return beverage_result


def change_beverage_on_hopper(
    current_id: int, new_drink_on_hopper_id: int, hopper_id: int
):
    """allocates a new drink on the hopper by changing the hopper_id"""

    change_drink_id_on_hopper(hopper_id, new_drink_on_hopper_id)


def get_all_available_mixed_drinks() -> list[runtime_data.MixDrinkInformation]:
    """returns a list of mix_drink_information objects
    consisting of all mix_drinks which can be mixed"""

    drink_list: dict = get_drink_list()
    dispensable_mix_drinks: list[runtime_data.MixDrinkInformation] = []

    for drink_id in drink_list:
        if (drink_list[drink_id]["mix_drink"]) and (
            drink_list[drink_id]["dispensable"]
        ):
            dispensable_mix_drinks.append(create_mix_drink_object(drink_list[drink_id]))

    return dispensable_mix_drinks
    # create mix_drink_information object as a result


def get_all_mixed_drinks() -> list[runtime_data.MixDrinkInformation]:
    """returns a list of mix_drink_information objects
    consisting of all mix_drinks"""

    drink_list: dict = get_drink_list()
    dispensable_mix_drinks: list[runtime_data.MixDrinkInformation] = []

    for drink_id in drink_list:
        if drink_list[drink_id]["mix_drink"]:
            dispensable_mix_drinks.append(create_mix_drink_object(drink_list[drink_id]))

    return dispensable_mix_drinks


def is_name_available(__name: str) -> bool:
    """checks whether a given name is already used"""

    drink_list: dict = get_drink_list()
    name_available: bool = True

    for drink_id in drink_list:
        if drink_list[drink_id]["name"] == __name:
            name_available = False
            break

    return name_available


def save_cocktails(mix_drink_information: runtime_data.MixDrinkInformation) -> bool:
    """saves a new mix_drink to the drink_list"""

    name: str = mix_drink_information.m_name

    if is_name_available(name):
        mix_drink_id: int = mix_drink_information.m_id
        mix_drink_name: str = mix_drink_information.m_name
        mix_drink_fill_perc_beverages: list[
            list[int]
        ] = mix_drink_information.m_fill_percentage_to_beverage

        add_drink(
            mix_drink=True,
            new_drink_id=mix_drink_id,
            name=mix_drink_name,
            required_drinks=mix_drink_fill_perc_beverages,
        )
        return True
    else:
        return False


def close_connection():
    pass
