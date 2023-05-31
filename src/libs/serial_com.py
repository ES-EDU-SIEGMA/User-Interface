import time
from . import globals as local_globals

if local_globals.RUN_ON_PI:
    import serial
else:
    print("COM USING MOCK!")
    from . import mock_serial as serial

picoleft: serial.Serial = None
picoright: serial.Serial = None
picorondell: serial.Serial = None

standard_baudrate = 115200

running = False


# identify all picos
def identify_picos(pico0, pico1, pico2):
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
            if pos.startswith(b"LEFT"):
                print("found left")
                picoleft = pico
                break
            elif pos.startswith(b"RIGHT"):
                print("found right")
                picoright = pico
                break
            elif pos.startswith(b"RONDELL"):
                print("found rondell")
                picorondell = pico
                break
            elif pos.startswith(b"F"):
                print("error, trying again")
                n += 1
                time.sleep(5)
            else:
                raise Exception(f"pico sent unknown identifier: {pos}")

        if (
            picoleft is None and picoright is None and picorondell is None
        ):  # not one was found
            raise Exception("No pico could be identified!")


# wait until all picos send their ready signal
def wait_until_ready():
    global picoleft
    global picoright
    global picorondell

    readyPicos = 0
    print("waiting for ready signal")
    while readyPicos < 3:
        for pico in [picoright, picoleft, picorondell]:
            resp = pico.readline()
            print(resp)
            if resp.startswith(b"CALIBRATED"):
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
        pico0 = serial.Serial("/dev/ttyACM0", standard_baudrate)
        pico1 = serial.Serial("/dev/ttyACM1", standard_baudrate)
        pico2 = serial.Serial("/dev/ttyACM2", standard_baudrate)

        identify_picos(pico0, pico1, pico2)
        wait_until_ready()

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
        raise Exception("Connection was not setup correctly!")


# send the input to the pico with the correct id
def send_msg(pico, message_to_send):
    global picoleft
    global picoright
    global picorondell
    global running

    if running:
        try:
            if pico == 0 and picoleft is not None:
                picoleft.write(bytes(message_to_send, "utf-8"))
            elif pico == 1 and picoright is not None:
                picoright.write(bytes(message_to_send, "utf-8"))
            elif pico == 2 and picorondell is not None:
                picorondell.write(bytes(message_to_send, "utf-8"))
            else:
                raise Exception("index of pico is invalid")
        except Exception as error:
            raise error
    else:
        raise Exception("Connection was not setup correctly!")
