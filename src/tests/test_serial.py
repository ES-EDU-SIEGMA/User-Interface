import serial_com as sc
#import serial_mock as ac



""" the range for timing values is somewhere between 5000 to 50_000.
    5000 is a value for a very fast flowing drink like water and 50_000 for a very thick drink.

    the activation time is calculated as: standardActivationTime * flowSpeed * 1000
    standardActivationTime is a global constand that is set to 5 (idk why 5 or why it's needed)
    flowSpeed is a measurement of the individual liquids flowing speed and ranges between 1 to 10 (max 12)."""




def sendTestMsgPico(picoID: int, timing1:int, timing2:int, timing3:int, timing4:int):
    """ sents the individual timings to the given picoID 
            picoRight   := picoID 0
            picoLeft    := picoID 1
            picoRondell := picoID 2 """
        
    print(f"sending to picoID {picoID} timings {timing1} {timing2} {timing3} {timing4}")
    picoCmd = f"{timing1};{timing2};{timing3};{timing4};\n"
    sc.send_msg(picoID, picoCmd)



def sendTestMsgPicoList(picoID: int, timings: list[int,int,int,int]):
    """ sents the timing list to the given picoID 
            picoRight   := picoID 0
            picoLeft    := picoID 1
            picoRondell := picoID 2 """

    print(f"sending to picoID {picoID} timings {timings}")
    picoCmd = f"{timings[0]};{timings[1]};{timings[2]};{timings[3]};\n"
    sc.send_msg(picoID, picoCmd)



def sendTestMsgHopper(hopperID: int, timing: int):
    print(f"sending to hopper {hopperID} timing {timing}")

    cmd = [0,0,0,0]
    cmd[hopperID%4] = timing

    picoID = None
    if    hopperID<4: picoID = 1
    elif  hopperID>3 and hopperID<8: picoID = 0
    else: picoID = 2

    sendTestMsgPicoList(picoID, cmd)



def sendTestMsgAll(timing: int):
    print(f"sending to all hoppers the timing {timing}")
    sendTestMsgPicoList(0, [timing,timing,timing,timing])
    sendTestMsgPicoList(1, [timing,timing,timing,timing])
    sendTestMsgPicoList(2, [timing,timing,timing,timing])