# import serial
import time

pico_left = None
pico_right = None
pico_rondell = None

standard_baudrate = 115200

running = False


# identify all picos
def identify_picos(pico0, pico1, pico2):
    global pico_left
    global pico_right
    global pico_rondell

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
                pico_left = pico
                break
            elif pos == b"RIGHT\r\n":
                print("found right")
                pico_right = pico
                break
            elif pos == b"RONDELL\r\n":
                print("found rondell")
                pico_rondell = pico
                break
            elif pos == b"F\r\n":
                print("error, trying again")
                n += 1
                time.sleep(5)
            else:
                raise Exception("pico sent unknown identifier")

        if (
            pico_left is None and pico_right is None and pico_rondell is None
        ):  # not one was found
            raise Exception("pico could not be identified")


# wait until all picos send their ready signal
def wait_until_ready():
    global pico_left
    global pico_right
    global pico_rondell

    ready_picos = 0
    print("waiting for ready signal")
    while ready_picos < 3:
        for pico in [pico_right, pico_left, pico_rondell]:
            resp = pico.readline()
            print(resp)
            if resp == b"CALIBRATED\r\n":
                ready_picos += 1
    print("all picos are setup")


# initialize all the connections
def __init__():
    global pico_left
    global pico_right
    global pico_rondell
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
    global pico_left
    global pico_right
    global pico_rondell
    global running

    if running:
        try:
            pico_left.close()
            pico_right.close()
            pico_rondell.close()
        except Exception as error:
            raise error
    else:
        raise Exception("connection wasn't setup correctly")


# send the input to the pico with the correct drink_to_add_id
def send_msg(pico: int, input_msg: str):
    global pico_left
    global pico_right
    global pico_rondell
    global running

    if running:
        try:
            if pico == 0 and pico_left is not None:
                pico_left.write(bytes(input_msg, "utf-8"))
            elif pico == 1 and pico_right is not None:
                pico_right.write(bytes(input_msg, "utf-8"))
            elif pico == 2 and pico_rondell is not None:
                pico_rondell.write(bytes(input_msg, "utf-8"))
            else:
                raise Exception("index of pico is invalid")
        except Exception as error:
            raise error
    else:
        raise Exception("connection wasn't setup correctly")
