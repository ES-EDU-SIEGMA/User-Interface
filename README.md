# SIEGMA2223 - DrinkMixingMachine

This project is the GUI and backend for the DrinkMixingMachine.

<!-- TOC -->

# Table of contents

* [Desciption]()
* [Setup](#setup)
* [Configuration](#configuration)
* [data](#data-model)

## Description

The DrinkMixingMachine

## Setup

In order for the program to run properly on the pi, the following python libraries are needed:

- [RPI.GPIO](src/libs/scale/scale_hardware/hx711.py)
- [Serial](src/libs/hopper/communication_hardware/communication.py)

Running the code on a regular computer doesn't require any additional libraries.

## Configuration

The program can be configured by changing the [configuration.json](src/configuration.json) file.

configuration options:

- configure_glass_size: int = ml that the glass holds


- configure_measurements_per_scale_value: int = how many measurements are used for one scale value
- configure_[measurement_calculation_method](src/libs/scale/scale_hardware/hx711.py): str = "average" | "median"


- configure_test_scale_version: bool = use a different ui to test the scale
- configure_test_serial_version: bool = use a different ui to test the hoppers


- configure_[mock_communication](src/libs/hopper/communication_hardware/mock_communication.py): bool = use a mock for
  hopper communication
- configure_[mock_scale](src/libs/scale/scale_hardware/mock_hx711.py): bool = use a mock for scale measurements


- configure_[ui_type](src/libs/ui/userinterface.py): str = "ui_console" | "placeholder"


- configure_[ingredient_file_path](src/libs/data/data_json/ingredients.json): str = file path to the ingredient file
- configure_[recipe_file_path](src/libs/data/data_json/recipes.json): str = file path to the recipe


- configure_tiny: dict
- configure_ingredients: dict

## Data model

The machine differentiates between ingredients and recipes.

Ingredient:= a liquid that can be put on a hopper.  
Ingredient: dir = {<ingredient-name>: {flow_speed: int,amount: int, hopper_position: None | int}}

Recipe:= a liquid consisting of one or more ingredients that can be mixed into a drink.  
Recipe: dir = {<recipe-name>: {<ingredient-name>: {fill_amount: int}
