# SIEGMA2223 - DrinkMixingMachine

This project is the GUI and backend for the Drinkmixingmachine.

## INSTALLATION

In order for the program to run properly, you need the following python librarys:
- PyQt5
- Serial
- psycopg2

Database-Setup:  
The program works with a postgres database, which is run locally on the pi or the machine the code is currently running
on.
The program expects the Database to be desgined by the given entity-relationship diagram (
siegma2223db_entityrelations_diagram.py).
If there is a need to change out the database to a different type of database, only the dbcon.py script is to be
changed.
The connection information to the database can be found and changed in the __init__() function of the dbcon.py script.
This function has to be called before the database is used.

Pico Connection:  
If you experience that the wrong hoppers get activated, simply check the USB-Connections of the picos to the pi. The
Pico that controlls the

## GENERAL INFORMATION

The Database running on the Pi has the following login-data: user: admin, password: admin (yes we are serious)
Same goes with the Pi.

## USSAGE OF THE APPLICATION

When you start the application you will be greeted by the main window. On the left you can find a list of beverages and
mix drinks which are currently mixable. If you click
on one of those, there will be a pop up window which asks you to specify the drink size and will inform you of the
duration and progress of the mixing process (given you clicked
start mixing).
On the right you can find three buttons, the lowest one will exit the application, the middle one will open another
window which lets you change the occupation of the hoppers and the
highest one will let you create new cocktails.

Adding new beverages:  
Sadly there is no easy way to add a new beverage via the GUI. So you have to add them manually to the database. The
beverages are stored the table "drinkmixingmachine.beverages".
There you have to manually insert them, the information needed are the name of the beverage you are adding and the
flowspeed of the beverage. The flowspeed tells
the application how viscous the beverages is you are currently adding. This is a very important information, because if
the multiplier is too low, you are going to have
way less mixed into your drink then you wanted. A flowspeed of 1 corresponses to the flowspeed of tapwater. This value
acts like a multiplier, so the value 2 will make the machine
open the hopper twice as long.

## THE MIXING PROCESS

Once you selected a Beverage or Mixdrink you want mixed and specified the drinksize the application will look up all
information it needs to mix. It will then calculate
the time each hopper needs to be activated and trys to make it as parallel as possible. If everything is calculated it
will send those information to the corresponding pico.

The picos will accept a string ending with a new line ('\n') symbol. The string consists of the activation time of each
hopper with the first value beeing the first hopper
and so forth, seperated by a semicolomn. An example string would look something like this: "5000;11500;0;0;\n". This
string tells the pico to activate hopper 1 for 5000ms,
hopper 2 for 11500ms and the other two for 0ms.
  

  
