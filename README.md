# SIEGMA User Interface

This project provides the Python UI and backend for the Drink mixing machine.

## INSTALLATION

In order for the program to run properly, you need the following python librarys:

- [PyQt5](https://pypi.org/project/PyQt5/)
- [pyserial](https://pypi.org/project/pyserial/)
- [psycopg2](https://pypi.org/project/psycopg2/) if you want to run the tool with a postgres DB

### Database-Setup

The original version of the Program requires a postgres database to work.
This database can run locally on the pi or the machine the code is currently running
on.
The program expects the Database to be designed based on the given [SQL scheme](./drinkmixingmachine.sql).
If there is a need to change out the database to a different type of database, only the [dbcon.py](./src/libs/dbcon.py)
script has to be changed.
The connection information to the database can be found and changed in the `__init__()` function of
the [dbcon.py](./src/libs/dbcon.py) script.
This function has to be called before the database is used.

The Database running on the Pi has the following login-data: user: admin, password: admin (yes we are serious)
Same goes with the Pi.

## USAGE OF THE APPLICATION

When you start the application you will be greeted by the main window. On the left you can find a list of beverages and
mix drinks which are currently mixable.
If you click on one of those, there will be a pop-up window which asks you to specify the drink size and will inform you
of the duration and progress of the mixing process (given you clicked start mixing).
On the right you can find three buttons, the lowest one will exit the application, the middle one will open another
window which lets you change the occupation of the hoppers and the highest one will let you create new cocktails.

### Adding new beverages

Sadly there is no easy way to add a new Beverage via the GUI.
So you have to add them manually to the database.
The beverages are stored the table `drinkmixingmachine.beverages`.
There you have to manually insert them, the information needed are the name of the Beverage you are adding and the
flowspeed of the Beverage.
The flowspeed tells the application how viscous the beverages is you are currently adding.
This is a very important information, because if the multiplier is too low, you are going to have way less mixed into
your drink then you wanted.
A flowspeed of 1 corresponds to the flowspeed of tap water.
This value acts like a multiplier, so the value 2 will make the machine open the hopper twice as long.

### THE MIXING PROCESS

Once you selected a Beverage or Mix drink you want mixed and specified the drink size the application will look up all
information it needs to mix.
It will then calculate the time each hopper needs to be activated and trys to make it as parallel as possible.
If everything is calculated it will send those information to the corresponding pico.

Further information about the communication protocol between the Tiny2040 and the Raspberry Pi can be retrieved from the
[Documentation Repository](https://github.com/ES-EDU-SIEGMA/Documentation).