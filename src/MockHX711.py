"""
simulates HX711
"""

class MockHX711:
	def __init__(self, dout, pd_sck, gain=128):
		self.dout = dout
		self.pd_sck = pd_sck
		self.gain = gain
		self.offset = 1
		self.offset_b = 1
		self.reference_unit = 1
		self.reference_unit_b = 1
	
	def is_ready(self):
		return True
		
	def set_gain(self, gain):
		pass
		
	def get_gain(self):
		return gain
		
	def real_long(self):
		return 0
		
	def read_average(self, times=3):
		return 0
	
	def read median(self, times=3):
		return 0
	
	def get_value(self, times=3):
		return 0
	
	def get_value_A(self, times=3):
		return 0
		
	def get_value_B(self, times=3):
		return 0
	
	def get_weight(self, times=3):
		return 0
		
	def get_weight_A(self, times=3):
		return 0
		
	def get_weight_B(self, times=3):
		return 0
		
	def tare(self, times=15):
		pass
		
	def tare_A(self, times=15):
		pass
		
	def tare_B(self, times=15):
		pass
		
	def set_reading_format(self, byte_format="LSB", bit_format="MSB"):
		pass
		
	def set_offset(self, offset):
		self.offset=offset
		
	def set_offset_A(self, offset):
		self.offset=offset
		
	def set_offset_B(self, offset):
		self.offset=offset
		
	def get_offset(self):
		return self.offset
	
	def get_offset_A(self):
		return self.offset
		
	def get_offset_B(self):
		return self.offset_b

	def set_reference_unit(self, reference_unit):
		self.reference_unit = reference_unit
	
	def set_reference_unit_B(self, reference_unit):
		self.reference_unit_b = reference_unit
	
	def get_reference_unit(self):
		return self.reference_unit
		
	def get_reference_unit_a(self):
		return self.reference_unit
	
	def get_reference_unit_b(self):
		return self.reference_unit_b
		
	def power_down(self):
		pass
		
	def power_up(self):
		pass
		
	def reset(self):
		pass
