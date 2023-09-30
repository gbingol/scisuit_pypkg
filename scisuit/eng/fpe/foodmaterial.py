import math as _math
import numbers as _numbers
import numpy as _np

from enum import Enum

from .wateractivity import Aw


class Food:
	pass



class Cp():
	pass


def Enthalpy(food:Food, Tf:float)->float:
	pass



class Fruit(Food):
	pass

class Vegetable(Food):
	pass

class Dairy(Food):
	pass

class Juice(Food):
	pass

class Beverage(Food):
	pass

class Meat(Food):
	pass

class Candy(Food):
	pass


class FoodType(Food, Enum):
	fruit = Fruit()
	vegetable = Vegetable()
	dairy = Dairy()
	juice = Juice()
	beverage = Beverage()
	meat = Meat()
	candy = Candy()



#-----------------------------------------------------------------------------

class Food:
	"""A class to compute thermal and physical properties of food materials"""
	
	def __init__(self, 
			water=0.0, 
			cho=0.0, 
			protein=0.0, 
			lipid=0.0, 
			ash=0.0, 
			salt=0.0, 
			group:FoodType = None):
		"""
		## Input: 
		water, cho, protein, lipid, ash, salt: % or fractions (must be consistent)
		group: Type of the food

		## Example:
		f1 = Food(cho=30, water=70) \n
		f2 = Food(cho=0.3, water=0.7)
		"""
		isOK = water>=0 and cho>=0 and protein>=0 and lipid>=0 and ash>=0 and salt>=0
		assert isOK, "Ingredients cannot have negative value."

		self._Water = water
		self._CHO = cho
		self._Protein = protein
		self._Lipid = lipid
		self._Ash = ash
		self._Salt = salt
		
		"""
		User does not necessarily provide values where total fraction is exactly 1.0
		Therefore it is adjusted so that total fraction is ALWAYS exactly 1.0
		
		Note that even if the values were percentages, dividing them
		by sum forces it to be in the range of [0, 1]
		"""
		Sum = self._Water + self._CHO + self._Protein + self._Lipid + self._Ash + self._Salt
		assert Sum>0, "At least one ingredient must be present"

		self._Water = self._Water/Sum
		self._CHO = self._CHO/Sum
		self._Protein = self._Protein/Sum
		self._Lipid = self._Lipid/Sum
		self._Ash = self._Ash/Sum
		self._Salt = self._Salt/Sum


		self._Ingredients = {
			"water":self._Water, "cho": self._CHO, "protein": self._Protein,
			"lipid":self._Lipid, "ash":self._Ash, "salt":self._Salt}
		
		filtered = {k:v for k, v in self._Ingredients.items() if v>0}
		self._Ingredients.clear()
		self._Ingredients.update(filtered)

		if group != None:
			assert isinstance(group, FoodType), "categ must be of type FoodType"
		self._group = group
		
		self._T = 20.0 # C
		self._Weight = 1.0 #Unit weight
		
			
	def __getitem__(self, index):
		return index
	


	def cp(self)->float:
		"""
		T is temperature in Celcius \n

		Thermo-physical properties are valid in the range of -40<=T(C) <=150
		2006, ASHRAE Handbook Chapter 9, Table 1 (source: Choi and Okos (1986))
		"""
		Cp_w = _np.polynomial.Polynomial([4.1289, -9.0864e-05, 5.4731e-06])
		Cp_p =  _np.polynomial.Polynomial([2.0082, 0.0012089, -1.3129e-06])
		Cp_f =  _np.polynomial.Polynomial([1.9842, 0.0014733, -4.8008e-06])
		Cp_CHO =  _np.polynomial.Polynomial([1.5488, 0.0019625, -5.9399e-06])
		Cp_ash =  _np.polynomial.Polynomial([1.0926, 0.0018896, -3.6817e-06])
		Cp_salt =  _np.polynomial.Polynomial([0.88])

		T = self._T

		return (self._Water)*Cp_w(T) + \
			(self._Protein)*Cp_p(T) + \
			(self._Lipid)*Cp_f(T) + \
			(self._CHO)*Cp_CHO(T) + \
			(self._Ash)*Cp_ash(T) +  \
			(self._Salt)*Cp_salt(T)



	def k(self)->float:
		"""result W/mK"""
		k_w =  _np.polynomial.Polynomial([0.57109, 0.0017625, -6.7036e-06])
		k_p =  _np.polynomial.Polynomial([0.17881, 0.0011958, -2.7178e-06])
		k_f =  _np.polynomial.Polynomial([0.18071, -0.00027604, -1.7749e-07])
		k_CHO =  _np.polynomial.Polynomial([0.20141, 0.0013874, -4.3312e-06])
		k_ash =  _np.polynomial.Polynomial([0.32962, 0.0014011, -2.9069e-06])
		k_salt =  _np.polynomial.Polynomial([0.574])
		"""
		For salt: 5.704 molal solution at 20C, Riedel L. (1962),
		Thermal Conductivities of Aqueous Solutions of Strong Electrolytes 
		Chem.-1ng.-Technik., 23 (3) P.59 - 64
		"""
		
		T=self._T

		return (self._Water)*k_w(T)+ \
			(self._Protein)*k_p(T) + \
			(self._Lipid)*k_f(T) + \
			(self._CHO)*k_CHO(T) + \
			(self._Ash)*k_ash(T) + \
			(self._Salt)*k_salt(T)	


	def conductivity(self)->float:
		"""Alias for k()"""
		return self.k()	
		
	
	def rho(self)->float:
		"""returns kg/m3"""
		rho_w =  _np.polynomial.Polynomial([997.18, 0.0031439, -0.0037574])
		rho_p =  _np.polynomial.Polynomial([1329.9, -0.5184])
		rho_f =  _np.polynomial.Polynomial([925.59, -0.41757])
		rho_CHO =  _np.polynomial.Polynomial([1599.1, -0.31046])
		rho_ash =  _np.polynomial.Polynomial([2423.8, -0.28063])
		rho_salt =  _np.polynomial.Polynomial([2165]) #Wikipedia
		
		T=self._T

		return (self._Water)*rho_w(T) + \
			(self._Protein)*rho_p(T) + \
			(self._Lipid)*rho_f(T) + \
			(self._CHO)*rho_CHO(T) + \
			(self._Ash)*rho_ash(T) + \
			(self._Salt)*rho_salt(T)


	def density(self)->float:
		"""Alias for rho()"""
		return self.rho()


	def aw(self)->float|None:
		"""
		Returns value of water activity or None \n
		
		## Warning:
		At T>25 C, built-in computation might return None. \n
		Therefore, must be used with caution.
		"""
		aw1 = 0.92
	
		water, cho, lipid, protein = self._Water, self._CHO, self._Lipid, self._Protein
		ash, salt = self._Ash, self._Salt 

		#note that salt is excluded
		Msolute = cho + lipid + protein + ash

		#There is virtually no water
		if water<0.01:
			return 0.01 
	
		#99.99% water
		if water>0.9999:
			return 1.0
	
		IsElectrolyte = salt>=0.1

		_aw = Aw(self)

		#Non-electrolytes solutions
		if not IsElectrolyte:
			# Dilute solution, as the total percentage is less than 1%
			if Msolute<0.01: 
				return 0.99
			
			#almost all CHO
			if cho>0.98:
				return 0.70

			#diluted
			if water>=0.70:
				aw1 = _aw.Raoult()

			#solute is 2.5 more times than solvent
			elif Msolute>=0.70:
				aw1 = _aw.Norrish()
			
			#most likely a candy
			elif lipid<0.01 and protein<0.01 and ash<0.01 and water>0.01 and water<0.05 and cho>0.05: 
				aw1 = _aw.MoneyBorn()	
			
			else:
				aw1 = _aw.FerroFontan_Chirife_Boquet()
	
		else:
			aw1 = _aw.Raoult()
	

		#somewhere around 20C
		if _math.isclose(self.temperature, 20, abs_tol=1E-1):
			return aw1

		#average molecular weight
		MWavg = water*18.02 + cho*180.16 + lipid*92.0944 + protein*89.09 + salt*58.44
	
		T = self.temperature

		self.temperature = 20
		Cp_20 = self.cp()

		self.temperature = T
		Cp_T = self.cp()

		Cp_avg = (Cp_20 + Cp_T) / 2.0	
		Qs = MWavg* Cp_avg*(T - 20.0) #kJ/kg
	
		R = 8.314 #kPa*m^3/kgK

		T += 273.15
		dT = 1/293.15 - 1/T
	
		aw2 = aw1*_math.exp(Qs/R*dT)
		
		return aw2 if aw2>=0 and aw2<=1 else None
	


	def h(self, T)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg \n
		T: Initial freezing temperature
		"""	 
		if(not isinstance(T, float)):
			raise TypeError("Initial freezing temperature must be of type float")
			
		return Enthalpy(self, T)


	def enthalpy(self, T)->float:
		"""Alias for h()"""
		return self.h(T)


	def freezing_T(self)->float|None:
		"""
		Estimates the initial freezing temperature of a food item \n
		returns in Celcius (None if estimation fails)
		"""
		water = self._Water 
		grp = self._group

		if grp != None:
			isMeat = (grp == FoodType.meat)
			isFruitVeg = (grp == FoodType.fruit) or (grp == FoodType.vegetable)
			isJuice =  (grp == FoodType.juice)

		#make educated guess
		else:
			isMeat =  _math.isclose(self._CHO, 0.0, abs_tol=1E-5)
			isFruitVeg = self._Lipid <0.1
			isJuice =  water>0.85
		
		if isMeat:
			return (271.18 + 1.47*water) - 273.15

		elif isFruitVeg:
			return (287.56 -49.19*water + 37.07*water**2) - 273.15

		elif isJuice:
			return 120.47 + 327.35*water - 176.49*water**2  - 273.15

		return None

	


	def x_ice(self, T:float)->float | None:
		"""
		Computes the fraction of ice \n
		T: Initial freezing temperature
		"""
		Tfood = self._T

		#if T_food > T then no ice can exist
		if Tfood > T:
			return None

		Tdiff = T -Tfood + 1

		#Tchigeov's (1979) equation (Eq #5 in ASHRAE manual)
		return 1.105*self._Water / (1 + 0.7138/_math.log(Tdiff))
	


	def makefrom(self, Foods:list)->list:
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
		"""
		sets the weight to 1.0
		"""
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
		return self._Water
	
	@property
	def cho(self)->float:
		return self._CHO

	@property
	def lipid(self)->float:
		return self._Lipid

	@property
	def protein(self)->float:
		return self._Protein

	@property
	def ash(self)->float:
		return self._Ash

	@property
	def salt(self)->float:
		return self._Salt



	#similar to mixing of two food items
	def __add__(self, foodB:Food)->Food:

		ma, mb = self.weight,  foodB.weight
		Ta, Tb = self.temperature, foodB.temperature 
		cpa, cpb = self.cp(), foodB.cp()

		water = ma*self.water + mb*foodB.water
		cho = ma*self.cho + mb*foodB.cho
		lipid = ma*self.lipid + mb*foodB.lipid
		protein = ma*self.protein + mb*foodB.protein
		ash = ma*self.ash + mb* foodB.ash
		salt = ma*self.salt + mb* foodB.salt

		sum = water + cho + lipid + protein + ash + salt

		retFood = Food(water=water/sum, cho=cho/sum, lipid=lipid/sum, protein=protein/sum, ash=ash/sum, salt=salt/sum)
		retFood.weight= ma + mb
	
		"""
		if the other food's temperature is negligibly different 
		then mixtures temperature is one of the food items' temperature
		"""
		if _math.isclose(Ta, Tb, rel_tol=1E-5):
			retFood.temperature = Ta	
		else:
			mtot = ma + mb
			E1 , E2 = ma*cpa*Ta, mb*cpb*Tb
			cp_avg = (ma*cpa + mb*cpb) / mtot
			Tmix = (E1 + E2)/(mtot*cp_avg)
		
			retFood.temperature = Tmix

		return retFood


	

	def __sub__(self, foodB:Food)->Food:	
		ma, mb = self.weight,  foodB.weight		
		if (ma - mb) < 0:
			raise ValueError("Weight must be >0")

		Ta, Tb = self.temperature, foodB.temperature
		if _math.isclose(Ta, Tb, rel_tol=1E-3) == False:
			raise ValueError("In subtraction foods' temperatures must be equal.")

		fA, fB = self.ingredients(), foodB.ingredients()
		newFood={}

		#A must have all the ingredients B has, check if it is the case
		for key, value in fB.items():
			if fA.get(key) == None:
				raise RuntimeError("Food does not have an ingredient:" + key)
		
		
		for key, value in fA.items():
			#Note that B does not need to have all the ingredients A has
			if fB.get(key) != None:	
				m_ingredient = ma*value - mb*fB[key]
				assert m_ingredient>=0, "Weight of " + key + " can not be smaller than zero"
				
				if(_math.isclose(m_ingredient, 0.0, abs_tol=1E-5)):
					m_ingredient=0
			else:
				m_ingredient = ma*value
			
			newFood[key] = m_ingredient


		Total = sum(newFood.values())
		for k,v in newFood.items():
			newFood[k] = float(v)/Total	

		retFood = Food(**newFood)
		retFood.weight = ma-mb

		return retFood




	def __mul__(self, elem:float)->Food:
		if not isinstance(elem, _numbers.Number):
			raise TypeError("Foods can only be multiplied by numbers")

		newFood = self.ingredients()
		retFood = Food(**newFood)

		retFood.weight = self.weight*elem

		return retFood




	def __rmul__(self, elem:float)->Food:
		if not isinstance(elem, _numbers.Number):
			raise TypeError("Foods can only be multiplied by numbers")
	 
		newFood = self.ingredients()
		retFood = Food(**newFood)

		retFood.weight = self.weight*elem

		return retFood

	

	def __str__(self):
		retStr=""

		retStr += "Weight (unit weight)=" + str(round(self.weight, 2)) +"\n"

		retStr += "Temperature (C)=" + str(round(self.temperature, 2)) +"\n"

		for k, v in self._Ingredients.items():
			retStr += f"{k} (%)= {str(round(v*100, 2))} \n"
		
		aw = self.aw()
		if aw != None:
			retStr +="aw=" + str(round(aw, 3)) + "\n"	

		return retStr


	
	def __eq__(self, foodB:Food)->bool:

		if not isinstance(foodB, Food):
			return False

		fA, fB = self.ingredients(), foodB.ingredients()

		#v is the value for fA and fB[k] returns corresponding key value in foodB
		for k,v in fA.items():
			"""
			if B does not have the same ingredient A has, then A and B cant be same
			"""
			if(fB.get(k) == None):
				return False
			
			"""
			values of the ingredient must be very close
			"""
			if not _math.isclose(v, fB[k], rel_tol=1E-5):
				return False
			
		return True
	

	def intersects(self, f2:Food)->bool:
		"""Do f1 and f2 have any common ingredient"""
		
		#ingredients return only the ingredients with value>0
		fA:dict = self.ingredients()
		fB:dict = f2.ingredients()

		for k, v in fA.items():
			if _math.isclose(v, fB[k], abs_tol=1E-3):
				return True
		
		return False
	



#-----------------------------------------------------------------------------

class Fruit(Food):
	def __init__(self, water=0.0, cho=0.0, protein=0.0, lipid=0.0, ash=0.0, salt=0.0):
		pass


class Vegetable(Food):
	def __init__(self, water=0.0, cho=0.0, protein=0.0, lipid=0.0, ash=0.0, salt=0.0):
		pass


class Dairy(Food):
	def __init__(self, water=0.0, cho=0.0, protein=0.0, lipid=0.0, ash=0.0, salt=0.0):
		pass


class Juice(Food):
	def __init__(self, water=0.0, cho=0.0, protein=0.0, lipid=0.0, ash=0.0, salt=0.0):
		pass


class Beverage(Food):
	def __init__(self, water=0.0, cho=0.0, protein=0.0, lipid=0.0, ash=0.0, salt=0.0):
		pass


class Meat(Food):
	def __init__(self, water=0.0, cho=0.0, protein=0.0, lipid=0.0, ash=0.0, salt=0.0):
		pass


class Candy(Food):
	def __init__(self, water=0.0, cho=0.0, protein=0.0, lipid=0.0, ash=0.0, salt=0.0):
		pass




#-------------------------------------------------------------------------------

class Cp():
	def __init__(self, food:Food) -> None:
		self._food = food

	def Siebel(self, Tf = -1.7)->float:
		"""
		returns kJ/kg°C \n

		## Input:
		Tf = -1.7 is the default freezing temperature

		## Reference:
		Siebel, E (1892). Specific heats of various products. Ice and Refrigeration, 2, 256-257.
		"""

		food = self._food

		Fat = food.lipid
		SNF = food.ash + food.protein + food.cho
		M = food.water
		Tfood = food.T


		#for fat free foods
		if _math.isclose(Fat, 0.0, abs_tol=1E-5):
			r = 837.36
			r += 3349*M if Tfood>Tf else 1256*M
			return r/1000

		r = 1674.72*Fat +  837.36*SNF
		r += 4186.8*M if Tfood>Tf else 2093.4*M

		return r/1000


	def Heldman(self)->float:
		"""
		returns kJ/kg°C 

		## Reference:
		Heldman, DR (1975). Food Process Engineering. Westport, CT: AVI 
		"""
		food = self._food

		Fat = food.lipid
		Protein = food.protein
		Ash = food.ash
		cho = food.cho
		water = food.water
		
		return 4.18*water + 1.547*Protein + 1.672*Fat + 1.42*cho + 0.836*Ash


	def Chen(self)->float:
		"""
		specific heat of an unfrozen food returns kJ/kg°C \n

		## Reference:
		Chen CS (1985). Thermodynamic Analysis of the Freezing and Thawing of Foods: 
		Enthalpy and Apparent Specific Heat. Food Science, 50(4), 1158-1162
		"""
		food = self._food

		Solid = 1 - food.water	
		return 4.19 - 2.30*Solid - 0.628*Solid**3



def Enthalpy(food:Food, Tf:float)->float:
	"""
	Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

	## Reference:
	2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

	## Notes:
	If foods current temperature smaller than Tfreezing it will 
	compute the enthalpy for frozen foods.
	
	Tf: Initial freezing temperature (a complete list available in ASHRAE)
	Vegetables: ~-1.5, 
	Fruits:~ -1.5 (Except dates=-15.7)
	Whole/shell fish: -2.2
	Beef: -1.7
	Milk: -0.6 (skim), -15.6 (evaporated, condensed)
	Juice/Beverages: -0.4
	"""

	assert isinstance(Tf, float), "Tfreezing must be float"

	LO = 333.6 #constant
	Tref= -40 #reference temperature

	Tfood=food.temperature

	water = food.water
	cho = food.cho
	lipid = food.lipid
	protein = food.protein
	ash = food.ash 
	salt = food.salt

	XWater = water

	XSolute = cho + lipid + protein + ash + salt

	"""
		if food's current T is smaller than or equal to (close enough) freezing temp 
		then it is assumed as frozen
	"""
	IsFrozen = Tfood<Tf or _math.isclose(Tfood,Tf, abs_tol=1E-5)

	if IsFrozen:
		"""
		If the food temperature is at 0C and it is frozen (IsFrozen = true)
		then return the enthalpy of ice at 0C
		"""
		if _math.isclose(Tfood,0.0, abs_tol=1E-5):
			return 2.050

		"""
		fraction of the bound water (Equation #3 in ASHRAE) (Schwartzberg 1976). 
		Bound water is the portion of water in a food that is bound to solids in the food, 
		and thus is unavailable for freezing.
		"""
		Xb = 0.4 * protein

		temp= 1.55 + 1.26* XSolute - (XWater - Xb) * (LO* Tf) / (Tref*Tfood)
		return (Tfood - Tref)*temp
	

	#UNFROZEN -> Equation #15 in ASHRAE book
	
	"""
	compute enthalpy of food at initial freezing temperature 
	Chang and Tao (1981) correlation, Eq #25 in ASHRAE manual
	"""
	Hf = 9.79246 + 405.096*XWater

	return Hf + (Tfood - Tf)*(4.19 - 2.30*XSolute - 0.628*XSolute**3) 