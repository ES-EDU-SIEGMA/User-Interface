"""

This class is to simulate the communication with the picos

"""

STANDARD_BAUDRATE = 115200

class SerialMock:
	def __init__(serf, port: str, baudrate: int):
		self.port = port
		self.baudrate = baudrate 
		self.responses = {
			"LEFT":   b"LEFT\r\n",
			"RIGHT":  b"RIGHT\r\n",
			"RONDELL":b"RONDELL\r\n",
			"CALIBRATED": b"CALIBRATED\r\n"
		}
		
		#use list as queue to simulate serial byte transfer
		self.buffer = []
		
		
	def readline(self) -> bytes:
		if self.buffer:
			return self.buffer.pop(0)
		else:
			return b''
			
	
	def write(self, input_data) -> None: 
		pass
		
	
	def close(self) -> None:
		pass
		
#from serialCom.py

picoleft = None
picoright = None
picorondell = None

