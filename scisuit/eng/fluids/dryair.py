import numbers as _numbers

class Air:
	def __init__(self, T:float, P:float=101325.0, Z:float=1.0) -> None:
		"""
		Properties of dry air

		## Input: 
		T: Temperature (K) \n
		P : Pressure (Pa) \n
		Z: Compressibility factor
		"""
		assert isinstance(T, _numbers.Real), "T must be real number"
		assert isinstance(P, _numbers.Real), "P must be real number"
		assert isinstance(Z, _numbers.Real), "Z must be real number"

		assert T>0, "T>0 expected"
		assert P>0, "P>0 expected"
		assert Z>0, "Z>0 expected"

		self._T=T
		self._P=P
		self._Z=Z

	
	def rho(self):
		"""return kg/m3, uses ideal gas equation with Z"""
		R = 287.0500676 #J/ (kg K)
		return self._P/(R*self._T*self._Z)
	
	def cp(self):
		"""
		returns kJ/kgK, does not take P and Z into account
		
		## Reference:
		Poling et al (2001). Properties of gases and liquids, 5th ed, McGraw-Hill
		"""
		T=self._T
		return (1030.5-0.19975*T+0.00039734*T**2)/1000
	
	def k(self):
		"""
		returns W/mK, does not take P and Z into account
		
		## Reference:
		Poling et al (2001). Properties of gases and liquids, 5th ed, McGraw-Hill
		"""
		T=self._T
		return (0.002334*T**1.5)/(164.54+T)
	
	def mu(self):
		"""
		returns Pa s, does not take P and Z into account
		
		## Reference:
		Sutherland equation
		"""
		T = self._T
		return (1.4592*T**1.5)/(109.1+T)*0.000001
	
	def Pr(self):
		"""Prandtl number"""
		return self.cp()*self.mu()/self.k()*1000
