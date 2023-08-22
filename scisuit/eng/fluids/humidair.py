
from ..._ctypeslib import coreDLL as _ctcore



class PsychrometryResult:
	"""
	Computation results of psychrometry class.

	## Example:
	>>result = psy.compute() \n
	>>result.P #access to pressure
	"""

	def __init__(self, psyresult):
		self.m_Results = psyresult

	def __str__(self) -> str:
		retStr=""

		if(len(self.m_Results)==0):
			return retStr

		retStr += "P=" + str(round(self.P, 2)) + " kPa" + "\n"

		retStr += "Tdb=" + str(round(self.Tdb, 2)) + " C" + "\n"
		
		retStr += "Twb=" + str(round(self.Twb, 2)) + " C" + "\n"
		
		retStr += "Tdp=" + str(round(self.Tdp, 2)) +  " C" + "\n"
		
		retStr += "H=" + str(round(self.H, 2)) + " kJ/kg da" + "\n"
		
		retStr += "RH=" + str(round(self.RH, 2)) + " %" + "\n"
		
		retStr += "W=" + str(round(self.W, 4)) +  " kg/kg da" + "\n"
		
		retStr += "V=" + str(round(self.V,3)) +  " m3/kg da" + "\n"

		return retStr


            
	@property
	def P(self): 
		"""Pressure in kPa"""
		
		return self.m_Results.get("P")


	@property
	def Tdb(self): 
		"""
		Dry bulb temperature in Celcius
		"""
		return self.m_Results.get("Tdb")

	@property
	def Twb(self): 
		"""
		Wet bulb temperature in Celcius
		"""
		return self.m_Results.get("Twb")

	@property
	def Tdp(self): 
		"""
		Dew point temperature in Celcius
		"""
		return self.m_Results.get("Tdp")

	@property
	def H(self):
		"""
		Enthalpy in kJ/kg da
		""" 
		return self.m_Results.get("H")

	@property
	def RH(self): 
		"""
		Relative Humidity in %
		"""
		return self.m_Results.get("RH")

	@property
	def W(self):
		"""
		Absolute Humidity in kg/kg da
		""" 
		return self.m_Results.get("W")

	@property
	def V(self): 
		"""
		Specific volume in m3/kg da
		"""
		return self.m_Results.get("V")

	@property
	def Pws(self):
		"""
		water vapor pressure at saturation in kPa
		"""
		return self.m_Results.get("Pws")

	@property
	def Pw(self):
		"""
		water vapor pressure in kPa
		"""
		return self.m_Results.get("Pw")

	@property
	def Ws(self):
		"""
		Absolute humidity at saturation kg/kg da
		"""
		return self.m_Results.get("Ws")



def psychrometry(**kwargs):
		
	"""
	Computes thermodynamic properties of humid-air.

	## Input: 
	3 keyword arguments containing only the following keys: \n
	1) P: Pressure (kPa)
	2) Tdb: Dry-bulb temperature (Celcius)
	3) Twb: Wet-bulb temperature (Celcius)
	4) Tdb: Wet-bulb temperature (Celcius)
	5) W: Absolute humidity (kg/kg da)
	6) RH: Relative humidity (%)
	7) H: Enthalpy (kJ/kg da)
	8) V: Specific Volume (m3/ kg da)

	## Example
	p=psychrometry(P=100, Tdb=50, RH=60) \n
	print(p) # prints all properties \n
	p.H # access only to enthalpy

	"""
	return PsychrometryResult(_ctcore.c_eng_psychrometry(kwargs))
