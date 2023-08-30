import numpy as _np


class Water:
	"""Thermo-physical properties of water."""

	def __init__(self, T:float) -> None:
		"""T in Celcius"""

		assert T>0 and T<100, "T must be in range (0, 100)"
		self.__T = T
	
	def cp(self)->float:
		"""
		Thermo-physical properties are valid in the range of -40<=T(C) <=150
		2006, ASHRAE Handbook Chapter 9, Table 1 (source: Choi and Okos (1986))
		"""
		Cp_w = _np.polynomial.Polynomial([5.4731E-6, -9.0864E-5, 4.1289][::-1])
		"""
		Note that previously scisuit.core polynomial was used and the list conforms
		to this (ax^n +... + a0). 
		However, new numpy polynomial uses reverse order and that's why [::-1]
		"""

		T = self.__T

		return Cp_w(T)
	

	def conductivity(self)->float:
		"""Thermal conductivity, result W/mK"""
		k_w =  _np.polynomial.Polynomial([-6.7036E-6, 1.7625E-3, 4.57109E-01][::-1])
		"""
		Note that previously scisuit.core polynomial was used and the list conforms
		to this (ax^n +... + a0). 
		However, new numpy polynomial uses reverse order and that's why [::-1]
		"""	
		T=self.__T

		return k_w(T)	

	
	def density(self)->float:
		"""returns kg/m3"""

		rho_w =  _np.polynomial.Polynomial([-3.7574E-3, 3.1439E-3, 997.18][::-1])
		"""
		Note that previously scisuit.core polynomial was used and the list conforms
		to this (ax^n +... + a0). 
		However, new numpy polynomial uses reverse order and that's why [::-1]
		"""	
		T=self.__T

		return rho_w(T)

	
	def viscosity(self)->float:
		"""
		returns Pa*s
		
		## Reference:
		Joseph Kestin, Mordechai Sokolov, and William A. Wakeham
		Viscosity of liquid water in the range -8°C to 150°C
		Journal of Physical and Chemical Reference Data 7, 941 (1978);	
		"""
		T=self.__T
		mu_ref=1002 #micro-Pascal*second (at 20C)
		
		temp1 =(20-T)/(T+96)*(1.2378-0.001303*(20-T)+0.00000306*(20-T)**2+0.0000000255*(20-T)**3)
		mu = 10**temp1*mu_ref #micro-Pascal*second
	
		return mu/1E6
	

	@property
	def T(self):
		"""in Celcius, same as property temperature"""
		pass

	@T.setter
	def T(self, T):
		assert T+273.15 >= 0, "Temperature > 0 Kelvin expected"
		self.__T = T

	@T.getter
	def T(self)->float:
		return self.__T
	

"""
if __name__ == "__main__":
	w=Water(30)
	print(w.viscosity())
	print(w.cp())
	print(w.conductivity())
	print(w.density())

	w.T=15
	print(w.viscosity())
	print(w.cp())
	print(w.conductivity())
	print(w.density())
"""