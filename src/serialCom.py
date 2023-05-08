import time
import sys
import os

#set the environment variable USE_MOCK=True before executing the coe
#export USE_MOCK=True (Linux)

USE_MOCK = os.environ.get("USE_MOCK", False)

if USE_MOCK:
	import SerialMock
else:
	import serial

picoleft = None
picoright = None
picorondell = None

standard_baudrate = 115200

running = False


# identify all picos
def identifyPicos(pico0, pico1, pico2):
    global picoleft
    global picoright
    global picorondell

    for pico in [pico0, pico1, pico2]:
        n = 0
        while n < 5:
            print("sending pico identifying request")
            pico.write(bytes("i\n", "utf-8"))

            print("waiting for identifier")
            pos = pico.readline()
            print(f"response was {pos}")
            if pos == b"LEFT\r\n":
                print("found left")
                picoleft = pico
                break
            elif pos == b"RIGHT\r\n":
                print("found right")
                picoright = pico
                break
            elif pos == b"RONDELL\r\n":
                print("found rondell")
                picorondell = pico
                break
            elif pos == b"F\r\n":
                print("error, trying again")
                n += 1
                time.sleep(5)
            else:
                raise Exception("pico sent unknown identifier")

        if (
            picoleft is None and picoright is None and picorondell is None
        ):  # not one was found
            raise Exception("pico could not be identified")


# wait until all picos send their ready signal
def waitUntilReady():
    global picoleft
    global picoright
    global picorondell

    readyPicos = 0
    print("waiting for ready signal")
    while readyPicos < 3:
        for pico in [picoright, picoleft, picorondell]:
            resp = pico.readline()
            print(resp)
            if resp == b"CALIBRATED\r\n":
                readyPicos += 1
    print("all picos are setup")


# initialize all the connections
def __init__():
    global picoleft
    global picoright
    global picorondell
    global running
    global standard_baudrate

    try:
		#acm = usb
        if MOCK:
            pico0 = SerialMock('/dev/ttyACM0_LEFT', standard_baudrate)
            pico1 = SerialMock('/dev/ttyACM2_RIGHT', standard_baudrate)
            pico2 = SerialMock('/dev/ttyACM3_RONDELL', standard_baudrate)
        else:
            pico0 = serial.Serial("/dev/ttyACM0", standard_baudrate)
            pico1 = serial.Serial("/dev/ttyACM1", standard_baudrate)
            pico2 = serial.Serial("/dev/ttyACM2", standard_baudrate)

        identifyPicos(pico0, pico1, pico2)
        waitUntilReady()

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


# send the input to the pico with the correct id
def send_msg(pico, input):
    global picoleft
    global picoright
    global picorondell
    global running

    if running:
        try:
            if pico == 0 and picoleft is not None:
                picoleft.write(bytes(input, "utf-8"))
            elif pico == 1 and picoright is not None:
                picoright.write(bytes(input, "utf-8"))
            elif pico == 2 and picorondell is not None:
                picorondell.write(bytes(input, "utf-8"))
            else:
                raise Exception("index of pico is invalid")
        except Exception as error:
            raise error
    else:
        raise Exception("connection wasnt setup correctly")
