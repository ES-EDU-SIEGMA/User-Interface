import serial
import time
import sys

picoleft = None
picoright = None
picorondell = None

standard_baudrate = 115200

running = False

#initialize all the connections
def __init__():
    global picoleft
    global picoright
    global picorondell
    global running
    global standard_baudrate
    
    print("running")
    
    try:
        pico0 = serial.Serial('/dev/ttyACM0', standard_baudrate) # hopper 1-4 (left side)
        pico1 = serial.Serial('/dev/ttyACM1', standard_baudrate) # hopper 5-8 (right side)
        pico2 = serial.Serial('/dev/ttyACM2', standard_baudrate) # hopper 9-12 (rondell)
        
        for pico in [pico0, pico1, pico2]:
            pos = pico.read()
            print(pos)
            if pos == "LEFT":
                picoleft = pico
            elif pos == "RIGHT":
                picoright = pico
            elif pos == "RONDELL":
                picorondell = pico
            else:
                raise Exception("couldnt identify the pico")
        
        running = True
        
    except Exception as error:
        raise error
    
def close_connection():
    global picoleft
    global picoright
    global picorondell
    global running
    
    if running:
        try:
            picoleft.close()
            picoright.close()
            picorondell.close()
        except Exception as error:
            raise error
    else:
        raise Exception("connection wasnt setup correctly")


#send the input to the pico with the correct id
def send_msg(pico, input):
    global picoleft
    global picoright
    global picorondell
    global running

    if running:
        try:
            if pico == 0:
                picoleft.write(bytes(input, 'utf-8'))
            elif pico == 1:
                picoright.write(bytes(input, 'utf-8'))
            elif pico == 2:
                picorondell.write(bytes(input, 'utf-8'))
            else:
                raise Exception("index of pico is invalid")
        except Exception as error:
            raise error
    else:
        raise Exception("connection wasnt setup correctly")
    
    
