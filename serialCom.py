import serial
import time
import sys

pico0 = None
pico1 = None
pico2 = None

standard_baudrate = 115200

running = False

#initialize all the connections
def __init__():
    global pico0
    global pico1
    global pico2
    global running
    global standard_baudrate
    
    try:
        pico0 = serial.Serial('/dev/ttyACM0', standard_baudrate) # hopper 1-4 (left side)
        #pico1 = serial.Serial('/dev/ttyACM1', standard_baudrate) # hopper 5-8 (right side)
        #pico2 = serial.Serial('/dev/ttyACM2', standard_baudrate) # hopper 9-12 (rondell)
        
        running = True
        
    except Exception as error:
        raise error
    
def close_connection():
    global pico0
    global pico1
    global pico2
    global running
    
    if running:
        try:
            pico0.close()
            #pico1.close()
            #pico2.close()
        except Exception as error:
            raise error
    else:
        raise Exception("connection wasnt setup correctly")


#send the input to the pico with the correct id
def send_msg(pico, input):
    global pico0
    global pico1
    global pico2
    global running

    if running:
        try:
            if pico == 0:
                pico0.write(bytes(input, 'utf-8'))
            elif pico == 1:
                pico1.write(bytes(input, 'utf-8'))
            elif pico == 2:
                pico2.write(bytes(input, 'utf-8'))
            else:
                raise Exception("index of pico is invalid")
        except Exception as error:
            raise error
    else:
        raise Exception("connection wasnt setup correctly")
    
    