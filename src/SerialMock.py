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
			
	
	"""
	Picos are identified by the device they control.
	Then calibrated comes in the queue
	so that waitUnitlReady() is properly simulated.
	Failure case neglected. We create three objects
	and have three picos for now.
	"""
	def write(self, input_data) -> None: 
		if input_data == b'i\n':
			if "LEFT" in self.port:
				self.buffer.append(self.responses["LEFT", "CALIBRATED"])				
			elif "RIGHT" in self.port:
				self.buffer.append(self.responses["RIGHT", "CALIBRATED"])				
			elif "RONDELL" in self.port:
				self.buffer.append(self.responses["RONDELL", "CALIBRATED"])
					
	
	def close(self) -> None:
		pass
		
#from serialCom.py

picoleft = None
picoright = None
picorondell = None

