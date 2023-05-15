test programm starts by running test_main
Currently offers three possible cmds:
1. send the same timing to all hoppers
2. send one timing to an individual hopper
3. send four timings to one pico controller


PLS note that there isn't yet an implementation that stops
you from sending another command before the previous
command is finished.


Depending on the directory structure the serial_com path name might
need to be changed.


not yet implemented:
-interaction with the scale
-limiting interactions while other cmds are getting executed