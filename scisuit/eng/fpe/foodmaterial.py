from __future__ import annotations
import math as _math
import numbers as _numbers
import numpy as _np

from .foodproperty import Aw, ComputeAw_T
from ...decorators import override
from ..defs import Dielectric


"""
Tolerance for temperature differences
if less than tolerance food's temperatures assumed equal
"""
T_TOL = 0.1



#-----------------------------------------------------------------------------

class Food:
	"""A class to compute thermal and physical properties of food materials"""
	
	def __init__(
			self, 
			water=0.0, 
			cho=0.0, 
			protein=0.0, 
			lipid=0.0, 
			ash=0.0, 
			salt=0.0):
		"""
		## Input: 
		water, cho, protein, lipid, ash, salt: % or fractions (must be consistent)

		## Example:
		f1 = Food(cho=30, water=70) \n
		f2 = Food(cho=0.3, water=0.7)
		"""
		isOK = water>=0 and isinstance(water, _numbers.Real) and \
			cho>=0 and isinstance(cho, _numbers.Real) and \
			protein>=0 and isinstance(protein, _numbers.Real) and \
			lipid>=0 and isinstance(lipid, _numbers.Real) and \
			ash>=0 and isinstance(ash, _numbers.Real) and \
			salt>=0 and isinstance(salt, _numbers.Real)
			
		assert isOK, "Ingredients must have non-negative real values."

		self._water = water
		self._cho = cho
		self._protein = protein
		self._lipid = lipid
		self._ash = ash
		self._salt = salt
		
		"""
		User does not necessarily provide values where total fraction is exactly 1.0
		Therefore it is adjusted so that total fraction is ALWAYS exactly 1.0
		
		Note that even if the values were percentages, dividing them
		by sum forces it to be in the range of [0, 1]
		"""
		Sum = self._water + self._cho + self._protein + self._lipid + self._ash + self._salt
		assert Sum>0, "At least one ingredient must be present"

		self._water /= Sum
		self._cho /= Sum
		self._protein /= Sum
		self._lipid /= Sum
		self._ash /= Sum
		self._salt /= Sum


		self._Ingredients = {
			"water":self._water, "cho": self._cho, "protein": self._protein,
			"lipid":self._lipid, "ash":self._ash, "salt":self._salt}
		
		filtered = {k:v for k, v in self._Ingredients.items() if v>0}
		self._Ingredients.clear()
		self._Ingredients.update(filtered)
		
		self._T = 20.0 # C
		self._Weight = 1.0 #Unit weight
		
	


	def __eq__(self, other:Food)->bool:

		assert isinstance(other, Food), "Food can only be compared with Food"
		
		if type(self) != type(other):
			return False

		fA, fB = self.ingredients(), other.ingredients()

		for k,v in fA.items():
			#if B does not have the same ingredient A has, then A and B cant be same
			if fB.get(k) == None:
				return False
			
			#values of the ingredient must be very close
			if not _math.isclose(v, fB[k], rel_tol=1E-5):
				return False
			
		return True
			



	#similar to mixing of two food items
	def __add__(self, rhs:Food)->Food:

		ma, mb = self.weight,  rhs.weight
		Ta, Tb = self.T, rhs.T 
		cpa, cpb = self.cp(), rhs.cp()

		water = ma*self.water + mb*rhs.water
		cho = ma*self.cho + mb*rhs.cho
		lipid = ma*self.lipid + mb*rhs.lipid
		protein = ma*self.protein + mb*rhs.protein
		ash = ma*self.ash + mb* rhs.ash
		salt = ma*self.salt + mb* rhs.salt

		fd = Food(water=water, cho=cho, lipid=lipid, protein=protein, ash=ash, salt=salt)
		fd.weight= ma + mb
	
		"""
		if the other food's temperature is negligibly different (Ta=10, Tb=10.1)
		then mixtures temperature is one of the food items' temperature
		"""
		if _math.isclose(Ta, Tb, abs_tol=T_TOL):
			fd.T = Ta	
		else:
			mtot = ma + mb
			e1 , e2 = ma*cpa*Ta, mb*cpb*Tb
			cp_avg = (ma*cpa + mb*cpb) / mtot
			Tmix = (e1 + e2)/(mtot*cp_avg)
		
			fd.T = Tmix

		if type(self) != type(rhs):
			return fd
		
		obj = type(self)
		f = obj(**fd.ingredients())
		f.weight = fd.weight
		f.T = fd.T
		return f


	

	def __sub__(self, B:Food)->Food:
		assert type(self) == type(B), "Foods must have same type"

		ma, mb = self.weight,  B.weight		
		assert (ma - mb) > 0, "weight A > weight B expected"

		Ta, Tb = self.T, B.T
		assert _math.isclose(Ta, Tb, abs_tol=T_TOL), "Temperature differences must be negligible."

		fA, fB = self.ingredients(), B.ingredients()

		#A must have all the ingredients B has, check if it is the case
		for k, _ in fB.items():
			assert fA.get(k) != None, "Food does not have an ingredient:" + k
		
		
		#collect ingredients in a dictionary
		ingDict={}

		for k, v in fA.items():
			#Note that B does not need to have all the ingredients A has
			_ing = None
			if fB.get(k) != None:	
				_ing = ma*v - mb*fB[k]
				assert _ing>=0, "Weight of " + k + " can not be smaller than zero"
				
				if _math.isclose(_ing, 0.0, abs_tol=1E-5): _ing = 0
			else:
				_ing = ma*v
			
			ingDict[k] = _ing


		fd = Food(**ingDict)
		fd.weight = ma-mb
		
		obj = type(self)
		f = obj(**fd.ingredients())
		f.weight = fd.weight
		f.T = fd.T

		return f




	def __mul__(self, m:float)->Food:
		assert isinstance(m, _numbers.Number), "Foods can only be multiplied by numbers"

		obj = type(self)
		f = obj(**self.ingredients())
		f.weight = self.weight*m
		f.T = self.T

		return f




	def __rmul__(self, m:float)->Food:
		assert isinstance(m, _numbers.Number), "Foods can only be multiplied by numbers"

		obj = type(self)
		f = obj(**self.ingredients())
		f.weight = self.weight*m
		f.T = self.T

		return f

	

	def __str__(self):
		retStr ="Type = " + self.__class__.__name__ + "\n"
		retStr += "Weight (unit weight) = " + str(round(self.weight, 2)) +"\n"
		retStr += "Temperature (C) = " + str(round(self.temperature, 2)) +"\n"

		for k, v in self._Ingredients.items():
			retStr += f"{k} (%) = {str(round(v*100, 2))} \n"
		
		aw = self.aw()
		if aw != None:
			retStr +="aw = " + str(round(aw, 3)) + "\n"	

		return retStr




	def cp(self)->float:
		"""
		T is temperature in Celcius \n

		Thermo-physical properties are valid in the range of -40<=T(C) <=150
		2006, ASHRAE Handbook Chapter 9, Table 1 (source: Choi and Okos (1986))
		"""
		w = _np.polynomial.Polynomial([4.1289, -9.0864e-05, 5.4731e-06])
		p =  _np.polynomial.Polynomial([2.0082, 0.0012089, -1.3129e-06])
		f =  _np.polynomial.Polynomial([1.9842, 0.0014733, -4.8008e-06])
		cho =  _np.polynomial.Polynomial([1.5488, 0.0019625, -5.9399e-06])
		ash =  _np.polynomial.Polynomial([1.0926, 0.0018896, -3.6817e-06])
		salt =  0.88

		T = self.T

		return self.water*w(T) + self.protein*p(T) + self.lipid*f(T) + \
			self.cho*cho(T) + self.ash*ash(T) + self.salt*salt



	def k(self)->float:
		"""result W/mK"""
		w =  _np.polynomial.Polynomial([0.57109, 0.0017625, -6.7036e-06])
		p =  _np.polynomial.Polynomial([0.17881, 0.0011958, -2.7178e-06])
		f =  _np.polynomial.Polynomial([0.18071, -0.00027604, -1.7749e-07])
		cho =  _np.polynomial.Polynomial([0.20141, 0.0013874, -4.3312e-06])
		ash =  _np.polynomial.Polynomial([0.32962, 0.0014011, -2.9069e-06])
		salt =  0.574
		"""
		For salt: 5.704 molal solution at 20C, Riedel L. (1962),
		Thermal Conductivities of Aqueous Solutions of Strong Electrolytes 
		Chem.-1ng.-Technik., 23 (3) P.59 - 64
		"""
		
		T=self.T

		return self.water*w(T)+ self.protein*p(T) + self.lipid*f(T) + \
			self.cho*cho(T) + self.ash*ash(T) + self.salt*salt	


	def conductivity(self)->float:
		"""Alias for k()"""
		return self.k()	
		
	
	def rho(self)->float:
		"""returns kg/m3"""
		w =  _np.polynomial.Polynomial([997.18, 0.0031439, -0.0037574]) #water
		p =  _np.polynomial.Polynomial([1329.9, -0.5184]) #protein
		f =  _np.polynomial.Polynomial([925.59, -0.41757]) #lipid
		c =  _np.polynomial.Polynomial([1599.1, -0.31046]) #cho
		a =  _np.polynomial.Polynomial([2423.8, -0.28063]) #ash
		s =  2165 #salt, Wikipedia
		
		T=self.T

		return self.water*w(T) + self.protein*p(T) + self.lipid*f(T) + \
			self.cho*c(T) + self.ash*a(T) + self.salt*s


	def density(self)->float:
		"""Alias for rho()"""
		return self.rho()


	def aw(self)->float|None:
		"""
		Returns value of water activity or None \n
		
		## Warning:
		At T>25 C, built-in computation might return None. \n
		Therefore, must be used with caution at T>25.
		"""
		aw1 = 0.92
	
		water, cho, lipid, protein = self._water, self._cho, self._lipid, self._protein
		ash, salt = self._ash, self._salt 


		#Virtually no water or 99.99% water
		if water < 0.01 or water > 0.9999:
			return water
		
		#almost all CHO
		if cho>0.98:
			return 0.70

		#note that salt is excluded
		Msolute = cho + lipid + protein + ash

		# Dilute solution, as the total percentage is less than 1%
		if Msolute<0.01: 
			return 0.99
	

		"""This assumption is only valid for dilute ones"""
		IsElectrolyte = salt>=0.01

		_Aw = Aw(self)

		#Electrolytes solutions
		if IsElectrolyte:	
			aw1 = _Aw.Raoult()
			return ComputeAw_T(self, aw1)	
		
		#dilute
		if water>=0.90:
			aw1 = _Aw.Raoult()

		#solute is 2.5 more times than solvent
		elif Msolute>=0.70:
			aw1 = _Aw.Norrish()
		
		else:
			aw1 = _Aw.FerroFontan_Chirife_Boquet()

		return ComputeAw_T(self, aw1)
	


	def molecularweight(self)->float:
		"""
		Average molecular weight of the food item

		returns g/mol
		"""
		water, cho, lipid, protein = self._water, self._cho, self._lipid, self._protein
		salt = self._salt 
		
		return water*18.02 + cho*180.16 + lipid*92.0944 + protein*89.09 + salt*58.44



	def enthalpy(self, T)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

		## Input:
		T: Initial freezing temperature

		## Reference:
		2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

		## Notes:
		If foods current temperature smaller than Tfreezing it will 
		compute the enthalpy for frozen foods.
		"""	 			
		assert isinstance(T, float), "Initial freezing temperature must be float"

		LO = 333.6 #constant
		Tref= -40 #reference temperature

		Tfood=self.T

		X_w = self.water

		#solute
		X_slt = self.cho + self.lipid + self.protein + self.ash + self.salt 
	
		"""
		if food's current T is smaller than or equal to (close enough) freezing temp 
		then it is assumed as frozen
		"""
		IsFrozen = Tfood<T or _math.isclose(Tfood,T, abs_tol=T_TOL)

		if IsFrozen:
			"""
			If the food temperature is at 0C and it is frozen
			then return the enthalpy of ice at 0C
			"""
			if _math.isclose(Tfood,0.0, abs_tol=T_TOL):
				return 2.050

			"""
			fraction of the bound water (Equation #3 in ASHRAE) (Schwartzberg 1976). 
			Bound water is the portion of water in a food that is bound to solids in the food, 
			and thus is unavailable for freezing.
			"""
			Xb = 0.4 * self.protein

			temp= 1.55 + 1.26* X_slt - (X_w - Xb) * (LO* T) / (Tref*Tfood)
			return (Tfood - Tref)*temp
		

		#UNFROZEN -> Equation #15 in ASHRAE book
		
		"""
		compute enthalpy of food at initial freezing temperature 
		Chang and Tao (1981) correlation, Eq #25 in ASHRAE manual
		"""
		Hf = 9.79246 + 405.096*X_w

		return Hf + (Tfood - T)*(4.19 - 2.30*X_slt - 0.628*X_slt**3) 




	def freezing_T(self)->None:
		"""
		Estimates the initial freezing temperature of a food item \n
		returns in Celcius (None if estimation fails)

		## Warning:
		Not implemented in the base class (Food), raises error
		"""
		raise NotImplementedError("Only implemented for Juice, Fruit/Veggies and Meat")

	


	def x_ice(self, T:float)->float | None:
		"""
		Computes the fraction of ice \n
		T: Initial freezing temperature
		"""
		
		#if temperature > initial freezing temperature then no ice can exist
		if self.T > T:
			return None

		Tdiff = T -self.T + 1

		#Tchigeov's (1979) equation (Eq #5 in ASHRAE manual)
		return 1.105*self._water / (1 + 0.7138/_math.log(Tdiff))
	
	

	def dielectric(self, f:int = 2450)->Dielectric:
		"""
		Computes dielectric properties
		f: frequency in MHz

		## Reference:
		Gulati T, Datta AK (2013). Enabling computer-aided food process engineering: Property estimation
		equations for transport phenomena-based models, Journal of Food Engineering, 116, 483-504
		"""
		water = self._water 
		ash = self.ash
		T = self.T

		meat_dc = lambda w, ash: w*(1.0707-0.0018485*T) + ash*4.7947 + 8.5452
		meat_dl = lambda w, ash:  w*(3.4472-0.01868*T + 0.000025*T**2) + ash*(-57.093+0.23109*T) - 3.5985
		
		fv_dc = lambda w, ash:  38.57 + 0.1255 + 0.456*w - 14.54*ash - 0.0037*T*w + 0.07327*ash*T
		fv_dl = lambda w, ash: 17.72 - 0.4519*T + 0.001382*T**2 \
						- 0.07448*w + 22.93*ash - 13.44*ash**2 \
						+ 0.002206*w*T + 0.1505*ash*T

		#No generalized equation, so a crude approximation
		d_const = (meat_dc(water, ash) + fv_dc(water, ash)) / 2
		d_loss = (meat_dl(water, ash) + fv_dl(water, ash)) / 2
		
		return Dielectric(d_const, d_loss)
		


	def makefrom(self, Foods:list[Food])->list[float]:
		"""
		Given a list of food items, computes the amount of each to be mixed to 
		make the current food item \n
		Material Balance
		"""
		N = len(Foods)

		A, b = [], []
		A.append([1]*N) #first row is the weights
		b.append(1)

		for f in Foods:
			assert isinstance(f, Food), "All entries in the list must be of type Food"
			assert self.intersects(self, f), "List has food item with no common ingredient with the target"
		
		Ingredients = self.ingredients()
		NCols = len(Ingredients) + 1

		for key, value in Ingredients.items():
			row = []
			for f in Foods:
				ing = f.ingredients()
				val = 0.0
				if ing.get(key)!= None:
					val = ing[key]/100
				row.append(val)
			
			assert len(row) == NCols, "Malformed matrix"
			A.append(row)
			b.append(value/100*self.weight)

		#solve Ax=b
		return _np.linalg.solve(_np.asfarray(A), _np.asfarray(b)).tolist()



	def ingredients(self)->dict:
		return self._Ingredients
	

	def normalize(self):
		"""sets the weight to 1.0"""
		self._Weight = 1.0


	@property
	def temperature(self):
		"""in Celcius, same as property T"""
		pass

	@temperature.setter
	def temperature(self, T):
		assert T+273.15 >= 0, "Temperature > 0 Kelvin expected"
		self._T = T

	@temperature.getter
	def temperature(self)->float:
		return self._T
	
	@property
	def T(self):
		"""in Celcius, same as property temperature"""
		pass

	@T.setter
	def T(self, T):
		assert T+273.15 >= 0, "Temperature > 0 Kelvin expected"
		self._T = T

	@T.getter
	def T(self)->float:
		return self._T



	@property
	def weight(self):
		""" unit weight, NOT recommended to set the weight externally """
		pass

	@weight.setter
	def weight(self, weight:float):
		self._Weight=weight
	
	@weight.getter
	def weight(self)->float:
		return self._Weight


	@property
	def water(self)->float:
		return self._water
	
	@property
	def cho(self)->float:
		return self._cho

	@property
	def lipid(self)->float:
		return self._lipid

	@property
	def protein(self)->float:
		return self._protein

	@property
	def ash(self)->float:
		return self._ash

	@property
	def salt(self)->float:
		return self._salt

	

	def intersects(self, f2:Food)->bool:
		"""Do f1 and f2 have any common ingredient"""
		
		fA, fB = self.ingredients(), f2.ingredients()

		for k, v in fA.items():
			if _math.isclose(v, fB[k], abs_tol=1E-3):
				return True
		
		return False





#--------------------------------------------------------------------------------------

class Beverage(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)


	@override
	def freezing_T(self)->float|None:
		"""
		Estimates the initial freezing temperature of a food item \n
		returns in Celcius
		"""
		water = self._water 
		return 120.47 + 327.35*water - 176.49*water**2  - 273.15

	@override
	def enthalpy(self, T=-0.4)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

		## Input:
		T: Initial freezing temperature

		## Reference:
		2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

		## Notes:
		If foods current temperature smaller than Tfreezing it will 
		compute the enthalpy for frozen foods.
		
		"""	
		super().enthalpy(T) 			


#----------------------------------------------------------------------------------

class Juice(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)

	@override
	def freezing_T(self)->float|None:
		"""
		Estimates the initial freezing temperature of a food item \n
		returns in Celcius
		"""
		water = self._water 
		return 120.47 + 327.35*water - 176.49*water**2  - 273.15

	@override
	def enthalpy(self, T=-0.4)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

		## Input:
		T: Initial freezing temperature

		## Reference:
		2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

		## Notes:
		If foods current temperature smaller than Tfreezing it will 
		compute the enthalpy for frozen foods.
		"""
		super().enthalpy(T)


#----------------------------------------------------------------------------------------

class Cereal(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)


	@override
	def dielectric(self, f:int = 2450)->Dielectric:
		"""
		Computes dielectric properties
		f: frequency in MHz

		## Reference:
		Gulati T, Datta AK (2013). Enabling computer-aided food process engineering: Property estimation
		equations for transport phenomena-based models, Journal of Food Engineering, 116, 483-504
		"""
		w = self._water 
		
		#assuming it as bulk density
		logf = _math.log10(f)
		rho = self.rho()

		d_const = (1 + 0.504*w*rho/(_math.sqrt(w) + logf))**2
		d_loss = 0.146*rho**2 + 0.004615*w**2*rho**2*(0.32*logf + 1.74/logf - 1)
		
		return Dielectric(d_const, d_loss)



#----------------------------------------------------------------------------------------

class Legume(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)


	@override
	def dielectric(self, f:int = 2450)->Dielectric:
		"""
		Computes dielectric properties 
		f: frequency in MHz

		## Reference:
		Gulati T, Datta AK (2013). Enabling computer-aided food process engineering: Property estimation
		equations for transport phenomena-based models, Journal of Food Engineering, 116, 483-504
		"""
		w = self._water 
		
		#assuming it as bulk density
		logf = _math.log10(f)
		rho = self.rho()

		d_const = (1 + 0.504*w*rho/(_math.sqrt(w) + logf))**2
		d_loss = 0.146*rho**2 + 0.004615*w**2*rho**2*(0.32*logf + 1.74/logf - 1)
		
		return Dielectric(d_const, d_loss)



#----------------------------------------------------------------------------------------

class Nut(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)


	@override
	def dielectric(self, f:int = 2450)->Dielectric:
		"""
		Computes dielectric properties
		f: frequency in MHz

		## Reference:
		Gulati T, Datta AK (2013). Enabling computer-aided food process engineering: Property estimation
		equations for transport phenomena-based models, Journal of Food Engineering, 116, 483-504
		"""
		w = self._water 
		
		#assuming it as bulk density
		logf = _math.log10(f)
		rho = self.rho()

		d_const = (1 + 0.504*w*rho/(_math.sqrt(w) + logf))**2
		d_loss = 0.146*rho**2 + 0.004615*w**2*rho**2*(0.32*logf + 1.74/logf - 1)
		
		return Dielectric(d_const, d_loss)




#-------------------------------------------------------------------------------------

class Dairy(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)


	@override
	def enthalpy(self, T=-0.6)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

		## Input:
		T: Initial freezing temperature

		## Reference:
		2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

		## Notes:
		If foods current temperature smaller than Tfreezing it will 
		compute the enthalpy for frozen foods.
		
		Milk: -0.6 (skim), -15.6 (evaporated, condensed)
		"""	
		super().enthalpy(T)


#-----------------------------------------------------------------------------

class Fruit(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)
	
	@override
	def freezing_T(self)->float|None:
		"""
		Estimates the initial freezing temperature of a food item \n
		returns in Celcius
		"""
		water = self._water 	
		return (287.56 -49.19*water + 37.07*water**2) - 273.15
	

	@override
	def dielectric(self, f:int = 2450)->Dielectric:
		"""
		Computes dielectric properties
		f: frequency in MHz

		## Reference:
		Gulati T, Datta AK (2013). Enabling computer-aided food process engineering: Property estimation
		equations for transport phenomena-based models, Journal of Food Engineering, 116, 483-504
		"""
		water = self._water 
		ash = self.ash
		T = self.T
		
		fv_dc = lambda w, ash:  38.57 + 0.1255 + 0.456*w - 14.54*ash - 0.0037*T*w + 0.07327*ash*T
		fv_dl = lambda w, ash: 17.72 - 0.4519*T + 0.001382*T**2 \
						- 0.07448*w + 22.93*ash - 13.44*ash**2 \
						+ 0.002206*w*T + 0.1505*ash*T

		return Dielectric(fv_dc(water, ash), fv_dl(water, ash))


	@override
	def enthalpy(self, T=-1.5)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

		## Input:
		T: Initial freezing temperature

		## Reference:
		2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

		## Notes:
		If foods current temperature smaller than Tfreezing it will 
		compute the enthalpy for frozen foods.
		"""	
		super().enthalpy(T)

#--------------------------------------------------------------------------

class Vegetable(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)

	@override
	def freezing_T(self)->float|None:
		"""
		Estimates the initial freezing temperature of a food item \n
		returns in Celcius
		"""
		water = self._water 	
		return (287.56 -49.19*water + 37.07*water**2) - 273.15

	@override
	def dielectric(self, f:int = 2450)->Dielectric:
		"""
		Computes dielectric properties
		f: frequency in MHz

		## Reference:
		Gulati T, Datta AK (2013). Enabling computer-aided food process engineering: Property estimation
		equations for transport phenomena-based models, Journal of Food Engineering, 116, 483-504
		"""
		water = self._water 
		ash = self.ash
		T = self.T
		
		fv_dc = lambda w, ash:  38.57 + 0.1255 + 0.456*w - 14.54*ash - 0.0037*T*w + 0.07327*ash*T
		fv_dl = lambda w, ash: 17.72 - 0.4519*T + 0.001382*T**2 \
						- 0.07448*w + 22.93*ash - 13.44*ash**2 \
						+ 0.002206*w*T + 0.1505*ash*T

		return Dielectric(fv_dc(water, ash), fv_dl(water, ash))
	


	@override
	def enthalpy(self, T=-1.5)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

		## Input:
		T: Initial freezing temperature

		## Reference:
		2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

		## Notes:
		If foods current temperature smaller than Tfreezing it will 
		compute the enthalpy for frozen foods.
		"""	
		super().enthalpy(T)





#---------------------------------------------------------------------------------

class Meat(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)

	@override
	def freezing_T(self)->float|None:
		"""
		Estimates the initial freezing temperature of a food item \n
		returns in Celcius
		"""
		water = self._water 
		return (271.18 + 1.47*water) - 273.15


	@override
	def dielectric(self, f:int = 2450)->Dielectric:
		"""
		Computes dielectric properties
		f: frequency in MHz

		## Reference:
		Gulati T, Datta AK (2013). Enabling computer-aided food process engineering: Property estimation
		equations for transport phenomena-based models, Journal of Food Engineering, 116, 483-504
		"""
		water = self._water 
		ash = self.ash
		T = self.T
		
		meat_dc = lambda w, ash: w*(1.0707-0.0018485*T) + ash*4.7947 + 8.5452
		meat_dl = lambda w, ash:  w*(3.4472-0.01868*T + 0.000025*T**2) + ash*(-57.093+0.23109*T) - 3.5985
		
		return Dielectric(meat_dc(water, ash), meat_dl(water, ash))


	@override
	def enthalpy(self, T=-1.7)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

		## Input:
		T: Initial freezing temperature

		## Reference:
		2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

		## Notes:
		If foods current temperature smaller than Tfreezing it will 
		compute the enthalpy for frozen foods.
		"""	
		super().enthalpy(T)





#-------------------------------------------------------------------------------------
class Sweet(Food):
	def __init__(self, water=0, cho=0, protein=0, lipid=0, ash=0, salt=0):
		super().__init__(water, cho, protein, lipid, ash, salt)

	@override
	def aw(self)->float|None:
		"""
		Returns value of water activity or None \n

		## Warning:
		At T>25 C, built-in computation might return None. \n
		Therefore, must be used with caution.
		"""
		_aw = Aw(self)	
		return ComputeAw_T(self, _aw.MoneyBorn())


	@override
	def enthalpy(self, T=-15)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

		## Input:
		T: Initial freezing temperature

		## Reference:
		2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

		## Notes:
		If foods current temperature smaller than Tfreezing it will 
		compute the enthalpy for frozen foods.
		"""	
		super().enthalpy(T)
