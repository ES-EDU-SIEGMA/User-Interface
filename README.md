# SIEGMA2223 - DrinkMixingMachine - Python code

***

<!-- TOC -->

# Table of contents

* **[Requirements](#requirements)**
* **[Configuration](#configuration)**
* **[Program](#program)**
* **[Data model](#data-model)**
* **[Hopper](#hopper)**
* **[Scale](#scale)**
* **[Configuration-options](#configuration-options)**

<br>

***

<br>

## Requirements

> Running the code locally without hardware access:
>
> - Python version XXX
> - No additional modules needed


> Running the code on the pi:
>
> - Python version XXX
> -  module `Serial`  
> *The module Serial is used to communicate over UART with the tiny.*
> -  module `RPI.GPIO`  
> *The module RPI.GPIO is used to communicate with the hx711 over the pi GPIO pins.*
> -  submodule [`tatobari_hx711`](https://github.com/tatobari/hx711py)  
> *The submodule tatobari_hx711 is used to read out the scale value*

To update the tatobari_hx711 submodule run the following command:
```bash
git submodule update --init --recursive
```

#### References in code:
[Serial](src/libs/hopper/communication_hardware/communication.py)  
[RPI.GPIO](src/libs/scale/scale_interface.py)

#### tatobari_hx711 module github:
[hx_711](src/libs/scale/scale_hardware/tatobari_hx711)


<br>

***

<br>

## Configuration

The program can be configured by changing the [configuration.json](src/configuration.json) file.
See the [configuration options](#configuration-options) for an explanation.

> Options to run the code locally with hardware mocks:
>
> - configure_mock_communication: **false**
> - configure_mock_scale: **false**

<br>

***

<br>

## Program

![uml diagram program overview](/documentation/class%20diagram%20general%20overview%20program.png)

#### to run the program simply use:
```bash
python src/main.py
```

<br>

***

<br>

## Data model

#### General overview of the data model:
![data model uml diagram](/documentation/Data%20model.png)  
> #### Ingredient
> 
> - an ingredient is a  liquid that  can be put on a hopper.
> - [json ingredient file](src/libs/data/data_json/ingredients.json)
> ```json
> {
>    "ingredient_name": {
>       "flow_speed": "Integer_value"
>    }
> }
>```

> #### Recipe
> 
> - A recipe is a liquid consisting of one or more ingredients.
> - [json recipe file](src/libs/data/data_json/recipes.json) 
> ```json
> {
>    "recipe_name": {
>       "ingredient_name": {
>           "fill_amount":  "Integer_value"
>           }
>       }
> }
>```

<br>

***

<br>

## Hopper

#### General information:
- The hopper mechanism is controlled through tiny pico controllers.  
- To activate a hopper the pi communicates with a tiny.  
- Each tiny connects to 1 to 4 stepper motors that control one hopper each.  
- The connection between pi and tiny works over UART.
- The pi is connected to the tiny through his USB ports.

#### Connection initialization:
- The pi try's to initialize a connection with a tiny on each USB port that is named in the [configuration](#configuration-options).
- If a connection couldn't be established the pi will throw an error.
- After connecting to all tinys the pi will try to identify each tiny connection.
- The pi identifies a tiny if the string identifier send by the tiny is the same as those in the [configuration](#configuration-options).
- The pi will throw an error if an unknown identifier is received.

#### Tiny pico communication:


## Scale

<br>

***

<br>

## Configuration options

> #### "configuration_only_selection":
>
> - value: **Boolean**
> - runs a program that only consists of the drink selection (if value is true)

> #### "configure_glass_size":
>
> - value: **Integer**
> - ml amount that the glass holds
> - this value is used during the new recipe creation to check if a new recipe fits in the glass.
> - we are currently using ikea 350ml glasses

> #### "configure_measurements_per_scale_value":
>
> - value: **Integer**
> - each scale value is calculated as an average.
> - this configuration option determines how many measurements are combined to an average.
> - the value for this option is currently chosen arbitrarily at 5

> #### "configure_mock_communication":
>
> - value: **Boolean**
> - uses a mock for communication with the tinys (if value is true)

> #### "configure_mock_scale":
>
> - value: **Boolean**
> - uses a mock for the scale (if value is true)

> #### "configure_max_waiting_time":
>
> - value: **Integer**
> - this option limits the amount of time the machine waits for a drink to finish dispensing.
> - if current-waiting-time > max_waiting_time the machine will return to its normal operation.
> - this option is primarily used to limit the waiting time when using mocks.
> - when the code is run on the machine the max_waiting_time should be high enough
> to prevent early abortions of the dispense process.

> #### "configure_connection_pi_tiny":
>
> - value: **list [file_path]**
> - holds the file-path to every usb port on the pi from which a Serial connection to a tiny should be established.
> - throws an error if no connection could be established.

> #### "configure_pico_identifier":
>
> - value: **list [String]**
> - each tiny returns a string identifier which is used to differentiate the different tinys.
> - this option holds all string identifiers that the pi expects.
> - the pi throws an error if it receives an unknown identifier or an identifier is unused.

> #### "configure_max_serial_identifier_attempt":
>
> - value: **Integer**
> - limits the amount of times the pi will try to identify a pico
> - if the pi hasn't identified the pico after its max attempts it will throw an error.

> #### "configuration_ms_per_ml":
>
> - value: **Integer**
> - variable that is used to configure the calculation of hopper timings on the pi.

> #### "configuration_hopper_sizes":
>
> - value: **list [Integer | None]**
> - this option holds the hopper sizes for each hopper measured in ml.
> - list position n refers to hopper at position n
> - None refers to an empty hopper or no hopper at all.

> #### "configure_ingredient":
>
> - value: **file_path**
> - holds the file-path to the json file with the ingredients.
> - [ingredients file](src/libs/data/data_json/ingredients.json)

> #### "configure_recipe":
>
> - value: **file_path**
> - holds the file-path to the json file with the recipes.
> - [recipes file](src/libs/data/data_json/recipes.json)

> #### "configure_ingredients":
>
> - value: **Dictionary**
> - the dictionary holds the initial configuration of the hoppers with ingredients.
> 
> ```json
> {
>     "configure_ingredients": {
>         "ingredient_name": {
>             "hopper_position": "Integer_value",
>             "amount": "Integer_value"
>         }
>     }
> }
> ```


