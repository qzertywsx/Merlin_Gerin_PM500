import pymodbus
from pymodbus.pdu import ModbusRequest
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

class PM500:
	def __init__(self, port, baudrate, unit_id, currentScale=1.0):
		self.port = port
		self.baudrate = baudrate
		self.unit_id = unit_id
		self.currentScale = currentScale
		self.client = ModbusClient(port=self.port, baudrate=self.baudrate)

	def __str__(self):
		return "PM500 port: " + self.port + ", baudrate: " + str(self.baudrate) + ", unit_id: " + str(self.unit_id) + ", Connected: " + str(self.client.connected)

	def check_connection(self):
		try:
			self.client.connect()
			return self.client.connected
		except:
			return False
	
	def disconnect(self):
		self.client.close()

	def __getint32(self,data):
		try:
			return ModbusClient.convert_from_registers(data.registers, ModbusClient.DATATYPE.INT32)
		except:
			return False
	
	def __dataToVoltage(self,data):
		return self.__getint32(data)/100
	
	def __dataToCurrent(self,data):
		return self.__getint32(data)/1000
	
	def __dataToCosfi(self,data):
		return self.__getint32(data)/1000
	
	def __dataToPower(self,data):
		return self.__getint32(data)/100
	
	def __dataToEnergy(self,data):
		return self.__getint32(data)
	
	def __dataToFrequency(self,data):
		return self.__getint32(data)/100
		
	def __dataToHarminic(self,data):
		return data.registers[0]/1000
		
	def __dataToHour(self,data):
		return self.__getint32(data)/100
	
	def getSinglePhase(self):
		try:
			U     = self.__dataToVoltage(self.client.read_holding_registers(0x030e, 2, self.unit_id))
			I     = self.__dataToCurrent(self.client.read_holding_registers(0x0300, 2, self.unit_id))*self.currentScale
			P     = self.__dataToPower(  self.client.read_holding_registers(0x031e, 2, self.unit_id))*self.currentScale
			Q     = self.__dataToPower(  self.client.read_holding_registers(0x0324, 2, self.unit_id))*self.currentScale
			S     = self.__dataToPower(  self.client.read_holding_registers(0x032a, 2, self.unit_id))*self.currentScale
			Cosfi = self.__dataToCosfi(  self.client.read_holding_registers(0x0368, 2, self.unit_id))
			return {"U": U, "I": I, "P": P, "Q": Q, "S": S, "Cosfi": Cosfi}
		except Exception as e:
			return False
	
	def getVoltage(self):
		try:
			U12 = self.__dataToVoltage(self.client.read_holding_registers(0x0308, 2, self.unit_id))
			U23 = self.__dataToVoltage(self.client.read_holding_registers(0x030a, 2, self.unit_id))
			U31 = self.__dataToVoltage(self.client.read_holding_registers(0x030c, 2, self.unit_id))
			U1  = self.__dataToVoltage(self.client.read_holding_registers(0x030e, 2, self.unit_id))
			U2  = self.__dataToVoltage(self.client.read_holding_registers(0x0310, 2, self.unit_id))
			U3  = self.__dataToVoltage(self.client.read_holding_registers(0x0312, 2, self.unit_id))
			return {"U12": U12, "U23": U23, "U31": U31, "U1": U1, "U2": U2, "U3": U3}
		except Exception as e:
			return False
	
	def getCurrent(self):
		try:
			I1 = self.__dataToCurrent(self.client.read_holding_registers(0x0300, 2, self.unit_id))*self.currentScale
			I2 = self.__dataToCurrent(self.client.read_holding_registers(0x0302, 2, self.unit_id))*self.currentScale
			I3 = self.__dataToCurrent(self.client.read_holding_registers(0x0304, 2, self.unit_id))*self.currentScale
			In = self.__dataToCurrent(self.client.read_holding_registers(0x0306, 2, self.unit_id))*self.currentScale
			return {"I1": I1, "I2": I2, "I3": I3, "In": In}
		except Exception as e:
			return False
	
	def getTotalPower(self):
		try:
			P = self.__dataToPower(self.client.read_holding_registers(0x0316, 2, self.unit_id))*self.currentScale
			Q = self.__dataToPower(self.client.read_holding_registers(0x0318, 2, self.unit_id))*self.currentScale
			S = self.__dataToPower(self.client.read_holding_registers(0x031a, 2, self.unit_id))*self.currentScale
			return {"P": P, "Q": Q, "S": S}
		except Exception as e:
			return False
	
	def getActivePower(self):
		try:
			P1 = self.__dataToPower(self.client.read_holding_registers(0x031e, 2, self.unit_id))*self.currentScale
			P2 = self.__dataToPower(self.client.read_holding_registers(0x0320, 2, self.unit_id))*self.currentScale
			P3 = self.__dataToPower(self.client.read_holding_registers(0x0322, 2, self.unit_id))*self.currentScale
			return {"P1": P1, "P2": P2, "P3": P3}
		except Exception as e:
			return False
	
	def getReactivePower(self):
		try:
			Q1 = self.__dataToPower(self.client.read_holding_registers(0x0324, 2, self.unit_id))*self.currentScale
			Q2 = self.__dataToPower(self.client.read_holding_registers(0x0326, 2, self.unit_id))*self.currentScale
			Q3 = self.__dataToPower(self.client.read_holding_registers(0x0328, 2, self.unit_id))*self.currentScale
			return {"Q1": Q1, "Q2": Q2, "Q3": Q3}
		except Exception as e:
			return False
	
	def getApparentPower(self):
		try:
			S1 = self.__dataToPower(self.client.read_holding_registers(0x032a, 2, self.unit_id))*self.currentScale
			S2 = self.__dataToPower(self.client.read_holding_registers(0x032c, 2, self.unit_id))*self.currentScale
			S3 = self.__dataToPower(self.client.read_holding_registers(0x032e, 2, self.unit_id))*self.currentScale
			return {"S1": S1, "S2": S2, "S3": S3}
		except Exception as e:
			return False
	
	def getCosfi(self):
		try:
			Cosfi_Tot = self.__dataToCosfi(self.client.read_holding_registers(0x0366, 2, self.unit_id))
			Cosfi_1   = self.__dataToCosfi(self.client.read_holding_registers(0x0368, 2, self.unit_id))
			Cosfi_2   = self.__dataToCosfi(self.client.read_holding_registers(0x036a, 2, self.unit_id))
			Cosfi_3   = self.__dataToCosfi(self.client.read_holding_registers(0x036c, 2, self.unit_id))
			return {"Cosfi tot": Cosfi_Tot, "Cosfi 1": Cosfi_1, "Cosfi 2": Cosfi_2, "Cosfi 3": Cosfi_3}
		except Exception as e:
			return False
	
	def getEnergy(self):
		try:
			E_Active        = self.__dataToEnergy(self.client.read_holding_registers(0x0358, 2, self.unit_id))*self.currentScale
			E_Reactive      = self.__dataToEnergy(self.client.read_holding_registers(0x035a, 2, self.unit_id))*self.currentScale
			E_Apparent      = self.__dataToEnergy(self.client.read_holding_registers(0x035c, 2, self.unit_id))*self.currentScale
			E_ActiveMinus   = self.__dataToEnergy(self.client.read_holding_registers(0x035e, 2, self.unit_id))*self.currentScale
			E_ReactiveMinus = self.__dataToEnergy(self.client.read_holding_registers(0x0360, 2, self.unit_id))*self.currentScale
			return {"E active": E_Active, "E reactive": E_Reactive, "E apparent": E_Apparent, "E active-": E_ActiveMinus, "E reactive-": E_ReactiveMinus}
		except Exception as e:
			return False
	
	def getHour(self):
		try:
			return self.__dataToHour(self.client.read_holding_registers(0x0356, 2, self.unit_id))
		except Exception as e:
			return False
	
	def getFrequency(self):
		try:
			return self.__dataToFrequency(self.client.read_holding_registers(0x0314, 2, self.unit_id))
		except Exception as e:
			return False

	def getTHD(self):
		try:
			THD_U12 = self.__dataToHarminic(self.client.read_holding_registers(0x0904, 1, self.unit_id))
			THD_U23 = self.__dataToHarminic(self.client.read_holding_registers(0x0905, 1, self.unit_id))
			THD_U31 = self.__dataToHarminic(self.client.read_holding_registers(0x0906, 1, self.unit_id))
			THD_U1  = self.__dataToHarminic(self.client.read_holding_registers(0x0907, 1, self.unit_id))
			THD_U2  = self.__dataToHarminic(self.client.read_holding_registers(0x0908, 1, self.unit_id))
			THD_U3  = self.__dataToHarminic(self.client.read_holding_registers(0x0909, 1, self.unit_id))
			THD_I1  = self.__dataToHarminic(self.client.read_holding_registers(0x0900, 1, self.unit_id))*self.currentScale
			THD_I2  = self.__dataToHarminic(self.client.read_holding_registers(0x0901, 1, self.unit_id))*self.currentScale
			THD_I3  = self.__dataToHarminic(self.client.read_holding_registers(0x0902, 1, self.unit_id))*self.currentScale
			THD_In  = self.__dataToHarminic(self.client.read_holding_registers(0x0903, 1, self.unit_id))*self.currentScale
			return {"THD U12": THD_U12, "THD U23": THD_U23, "THD U31": THD_U31, "THD U1": THD_U1, "THD U2": THD_U2, "THD U3": THD_U3, "THD I1": THD_I1, "THD I2": THD_I2, "THD I3": THD_I3, "THD In": THD_In}
		except Exception as e:
			return False
	
	def getSinglePhaseTHD(self):
		try:
			THD_U = self.__dataToHarminic(self.client.read_holding_registers(0x0907, 1, self.unit_id))
			THD_I = self.__dataToHarminic(self.client.read_holding_registers(0x0900, 1, self.unit_id))*self.currentScale
			return {"THD U": THD_U, "THD I": THD_I}
		except Exception as e:
			return False
	
	def resetStat(self):
		try:
			self.client.write_register(0x0400, 0x9100, self.unit_id)
			return True
		except Exception as e:
			return False
