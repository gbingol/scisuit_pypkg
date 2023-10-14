
from .._ctypeslib import pydll as _pydll
from numbers import Real as _Real


class PsychrometryResult:
	"""
	Computation results of psychrometry class.

	## Example:
	>>result = psy.compute() \n
	>>result.P #access to pressure
	"""

	def __init__(self, psyresult):
		self._Results = psyresult

	def __str__(self) -> str:

		if(len(self._Results) == 0):
			return ""
		
		s=""
		s += "P=" + str(round(self.P, 2)) + " kPa" + "\n"
		s += "Tdb=" + str(round(self.Tdb, 2)) + " C" + "\n"	
		s += "Twb=" + str(round(self.Twb, 2)) + " C" + "\n"	
		s += "Tdp=" + str(round(self.Tdp, 2)) +  " C" + "\n"	
		s += "H=" + str(round(self.H, 2)) + " kJ/kg da" + "\n"	
		s += "RH=" + str(round(self.RH, 2)) + " %" + "\n"	
		s += "W=" + str(round(self.W, 4)) +  " kg/kg da" + "\n"	
		s += "V=" + str(round(self.V,3)) +  " m3/kg da" + "\n"

		return s


	@property
	def P(self): 
		"""Pressure in kPa"""
		return self._Results.get("P")

	@property
	def Tdb(self): 
		"""Dry bulb temperature in Celcius"""
		return self._Results.get("Tdb")

	@property
	def Twb(self): 
		"""Wet bulb temperature in Celcius"""
		return self._Results.get("Twb")

	@property
	def Tdp(self): 
		"""Dew point temperature in Celcius"""
		return self._Results.get("Tdp")

	@property
	def H(self):
		"""Enthalpy in kJ/kg da""" 
		return self._Results.get("H")

	@property
	def RH(self): 
		"""Relative Humidity in %"""
		return self._Results.get("RH")

	@property
	def W(self):
		"""Absolute Humidity in kg/kg da""" 
		return self._Results.get("W")

	@property
	def V(self): 
		"""Specific volume in m3/kg da"""
		return self._Results.get("V")

	@property
	def Pws(self):
		"""water vapor pressure at saturation in kPa"""
		return self._Results.get("Pws")

	@property
	def Pw(self):
		"""water vapor pressure in kPa"""
		return self._Results.get("Pw")

	@property
	def Ws(self):
		"""Absolute humidity at saturation kg/kg da"""
		return self._Results.get("Ws")



def psychrometry(
		P:_Real=None,
		Tdb:_Real=None, 
		Twb:_Real=None, 
		Tdp:_Real=None, 
		W:_Real=None, 
		RH:_Real=None, 
		H:_Real=None, 
		V:_Real=None):
		
	"""
	Computes thermodynamic properties of humid-air.\n 
	Only 3 parameters must have Real values

	## Input: 
	P: Pressure (kPa)
	Tdb, Twb, Tdp: Dry-bulb, wet-bulb and dew point temperatures (°C)
	W, RH: Absolute(kg/kg da) and relative humidity (%)
	H: Enthalpy (kJ/kg da)
	V: Specific Volume (m3/ kg da)

	## Example
	p=psychrometry(P=100, Tdb=50, RH=60) \n
	print(p) # prints all properties \n
	p.H # access only to enthalpy

	"""
	d = {"P": P, "Tdb":Tdb, "Twb":Twb, "Tdp":Tdp, "W":W, "RH":RH, "H":H, "V":V}

	filtered = {k:v for k, v in d.items() if isinstance(v, _Real)}
	assert len(filtered)==3, "Exactly 3 parameters with real values expected."

	return PsychrometryResult(_pydll.c_eng_psychrometry(filtered))
