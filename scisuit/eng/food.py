import math as _math
import numbers as _numbers
import numpy as _np


class Food:
	pass



def Cp_Siebel(food:Food, Tfreezing = -1.7)->float:
	"""
	returns kJ/kg°C \n

	## Input:
	Tfreezing = -1.7 is the default freezing temperature

	## Reference:
	Siebel, E (1892). Specific heats of various products. Ice and Refrigeration, 2, 256-257.
	"""
	Fat = food.Lipid
	SNF = food.Ash + food.Protein + food.CHO
	M = food.Water
	Tfood:float = food.T


	#for fat free foods
	if(_math.isclose(Fat, 0.0, abs_tol=1E-5)):
		retVal = 837.36
		retVal += 3349*M if Tfood>Tfreezing else 1256*M
		return retVal/1000

	retVal = 1674.72*Fat +  837.36*SNF
	retVal += 4186.8*M if Tfood>Tfreezing else 2093.4*M

	return retVal/1000


def Cp_Heldman(food:Food):
	"""
	returns kJ/kg°C 

	## Reference:
	Heldman, DR (1975). Food Process Engineering. Westport, CT: AVI 
	"""
	Fat = food.Lipid
	Protein = food.Protein
	Ash = food.Ash
	CHO = food.CHO
	M = food.Water
	
	return 4.18*M + 1.547*Protein + 1.672*Fat + 1.42*CHO + 0.836*Ash


def Cp_Chen(food:Food)->float:
	"""
	specific heat of an unfrozen food returns kJ/kg°C \n

	## Reference:
	Chen CS (1985). Thermodynamic Analysis of the Freezing and Thawing of Foods: 
	Enthalpy and Apparent Specific Heat. Food Science, 50(4), 1158-1162
	"""
	Solid = 1 - food.Water	
	return 4.19 - 2.30*Solid - 0.628*Solid**3



def _Enthalpy(food:Food, Tfreezing:float)->float:
	"""
	Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg 

	## Reference:
	2006 ASHRAE Handbook, thermal properties of foods (Eq #18)

	## Notes:
	If foods current temperature smaller than Tfreezing it will 
	compute the enthalpy for frozen foods.
	
	Tfreezing: Initial freezing temperature (a complete list available in ASHRAE)
	Vegetables: ~-1.5, 
	Fruits:~ -1.5 (Except dates=-15.7)
	Whole/shell fish: -2.2
	Beef: -1.7
	Milk: -0.6 (skim), -15.6 (evaporated, condensed)
	Juice/Beverages: -0.4
	"""

	assert isinstance(Tfreezing, float), "Tfreezing must be float"

	LO = 333.6 #constant
	Tref= -40 #reference temperature

	Tfood=food.temperature

	water = food.Water
	CHO = food.CHO
	lipid = food.Lipid
	protein = food.Protein
	ash = food.Ash 
	salt = food.Salt

	XWater = water

	XSolute = CHO + lipid + protein + ash + salt

	"""
		if food's current T is smaller than or equal to (close enough) freezing temp 
		then it is assumed as frozen
	"""
	IsFrozen = Tfood<Tfreezing or _math.isclose(Tfood,Tfreezing, abs_tol=1E-5)

	if(IsFrozen):
		"""
		If the food temperature is at 0C and it is frozen (IsFrozen = true)
		then return the enthalpy of ice at 0C
		"""
		if(_math.isclose(Tfood,0.0, abs_tol=1E-5)):
			return 2.050

		"""
		fraction of the bound water (Equation #3 in ASHRAE) (Schwartzberg 1976). 
		Bound water is the portion of water in a food that is bound to solids in the food, 
		and thus is unavailable for freezing.
		"""
		Xb = 0.4 * protein

		temp= 1.55 + 1.26* XSolute - (XWater - Xb) * (LO* Tfreezing) / (Tref*Tfood)
		return (Tfood - Tref)*temp
	

	#UNFROZEN -> Equation #15 in ASHRAE book
	
	"""
	compute enthalpy of food at initial freezing temperature 
	Chang and Tao (1981) correlation, Eq #25 in ASHRAE manual
	"""
	Hf = 9.79246 + 405.096*XWater

	return Hf + (Tfood - Tfreezing)*(4.19 - 2.30*XSolute - 0.628*XSolute**3) 





def aw_FerroFontan_Chirife_Boquet(food:Food)->float:
	"""
	CHO is considered as fructose \n
	protein is considered as alanine \n
	lipid is considered as glycerol
	"""
	MW_CHO = 180.16
	MW_Lipid = 92.0944
	MW_Protein = 89.09

	NCHO, NLipid, NProtein = food.CHO/MW_CHO, food.Lipid/ MW_Lipid, food.Protein/MW_Protein
	NWater = food.Water/18.02
	Nsolute = NCHO + NLipid + NProtein

	Solute = 1 - food.Water
	C_CHO, C_Lipid, C_Protein = food.CHO/Solute, food.Lipid/Solute, food.Protein/Solute

	Mt= _math.sqrt(C_CHO/MW_CHO + C_Lipid/MW_Lipid + C_Protein/MW_Protein)

	# Norrish equation K values using Ferro-Chirife-Boquet equation
	Km = C_CHO*(Mt/MW_CHO)*(-2.15) +C_Lipid*(Mt/MW_Lipid)*(-1.16) + C_Protein*(Mt/MW_Protein)*(-2.52) 
	
	# Mole fraction of solute
	XSolute = Nsolute/(Nsolute + NWater) 

	# Mole fraction of water
	XWater = NWater/(Nsolute + NWater) 

	aw = XWater*_math.exp(Km*XSolute**2)

	return aw



def aw_Norrish(food:Food)->float:
	"""Norrish equation"""
	
	#CHO is considered as fructose
	NCHO = food.CHO/180.16 
	
	#lipid is considered as glycerol
	NLipid = food.Lipid/ 92.0944 
	
	#protein is considered as alanine
	NProtein = food.Protein/89.09 
	Nsolute = NCHO + NLipid + NProtein
	NWater = food.Water / 18
	NTotal = NCHO + NLipid + NProtein + NWater

	XCHO, XLipid, XProtein, XWater = NCHO/NTotal, NLipid/NTotal, NProtein/NTotal, NWater/NTotal

	
	# Norrish equation K values using Ferro-Chirife-Boquet equation
	SumSq = -(2.15)*XCHO**2 - (1.16)*XLipid**2 - (2.52)*XProtein**2
	SumX2 = XCHO**2 + XLipid**2 + XProtein**2
	
	RHS = _math.log(XWater) + SumSq/SumX2*(1-XWater)**2

	return _math.exp(RHS)



#mostly used in confectionaries
def aw_MoneyBorn(confectionary:Food)->float:
	# amount of CHO in 100 g water (equation considers thus way) 
	WeightCHO = 100*confectionary.CHO/confectionary.Water 
	
	#CHO is considered as fructose
	NCHO = WeightCHO/180.16 
	
	return 1.0/(1.0 + 0.27*NCHO)


def aw_Raoult(food:Food)->float:
	#prediction using Raoult's law
	#all in percentages
	xwater, xCHO, xlipid, xprotein, xash = food.Water, food.CHO, food.Lipid, food.Protein, food.Ash
	xsolute = xCHO + xlipid + xprotein + xash
	xsalt = food.Salt

	#average molecular weight
	if xsolute>0:
		MWavg_solute = (xCHO/xsolute)*180.16 + (xlipid/xsolute)*92.0944 + (xprotein/xsolute)*89.09
	else:
		MWavg_solute = 1
		
	MW_Water=18
	MW_NaCl = 58.44

	temp1 = xwater+(MW_Water/MWavg_solute)*xsolute + 2*(MW_Water/MW_NaCl)*xsalt

	return xwater/temp1




def HasIntersection(f1:Food, f2:Food)->int:
	"""return the number of common ingredients between f1 and f2"""
	
	#check if there are common ingredients
	fA, fB = f1.getIngredients(), f2.getIngredients()

	NamesA, NamesB = set(), set()
	for k in fA.keys():
		NamesA.add(k)

	for k in fB.keys():
		NamesB.add(k)

	return True if len(NamesA.intersection(NamesB))>0 else False



def Intersection(f1:Food, f2:Food)->list:
	"""return the name of common ingredients between f1 and f2"""
	
	if(not HasIntersection(f1, f2)):
		return []

	fA, fB = f1.getIngredients(), f2.getIngredients()

	Ingredients = []
		
	for k, v in fA.items():
		if(fB.get(k) != None):
			Ingredients.append(k)

	return Ingredients



class Food:
	"""
	A class to compute thermal and physical properties of food materials \n

	## Input: 
	Keys are CHO, protein, lipid(fat, oil), ash, Water, salt \n
	Values can be percentages or fractions (must be consistent) \n

	## Example:
	f = Food(CHO=30, water=70)
	"""
	
	def __init__(self, water=0.0, cho=0.0, protein=0.0, lipid=0.0, ash=0.0, salt=0.0):
		
		assert water>=0, "water must be >=0.0"
		assert cho>=0, "cho must be >=0.0"
		assert protein>=0, "protein must be >=0.0"
		assert lipid>=0, "lipid must be >=0.0"
		assert ash>=0, "ash must be >=0.0"
		assert salt>=0, "salt must be >=0.0"

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

		self._Water = self._Water/Sum
		self._CHO = self._CHO/Sum
		self._Protein = self._Protein/Sum
		self._Lipid = self._Lipid/Sum
		self._Ash = self._Ash/Sum
		self._Salt = self._Salt/Sum


		self.__Ingredients = {
			"water":self._Water, "cho": self._CHO, "protein": self._Protein,
			"lipid":self._Lipid, "ash":self._Ash, "salt":self._Salt}
		
		self._m_T = 20.0 # C
		self._m_Weight = 1.0 #Unit weight
		
			
	def __getitem__(self, index):
		return index
	


	def cp(self)->float:
		"""
		T is temperature in Celcius \n

		Thermo-physical properties are valid in the range of -40<=T(C) <=150
		2006, ASHRAE Handbook Chapter 9, Table 1 (source: Choi and Okos (1986))
		"""
		Cp_w = _np.polynomial.Polynomial([5.4731E-6, -9.0864E-5, 4.1289][::-1])
		Cp_p =  _np.polynomial.Polynomial([-1.3129E-6, 1.2089E-3, 2.0082][::-1])
		Cp_f =  _np.polynomial.Polynomial([-4.8008E-6, 1.4733E-3, 1.9842][::-1])
		Cp_CHO =  _np.polynomial.Polynomial([-5.9399E-6, 1.9625E-3, 1.5488][::-1])
		Cp_ash =  _np.polynomial.Polynomial([-3.6817E-6, 1.8896E-3, 1.0926][::-1])
		Cp_salt =  _np.polynomial.Polynomial([0.88])
		"""
		Note that previously scisuit.core polynomial was used and the list conforms
		to this (ax^n +... + a0). 
		However, new numpy polynomial uses reverse order and that's why [::-1]
		"""

		T = self._m_T

		return (self._Water)*Cp_w(T) + \
			(self._Protein)*Cp_p(T) + \
			(self._Lipid)*Cp_f(T) + \
			(self._CHO)*Cp_CHO(T) + \
			(self._Ash)*Cp_ash(T) +  \
			(self._Salt)*Cp_salt(T)



	def k(self)->float:
		"""result W/mK"""
		k_w =  _np.polynomial.Polynomial([-6.7036E-6, 1.7625E-3, 5.7109E-01][::-1])
		k_p =  _np.polynomial.Polynomial([-2.7178E-6, 1.1958E-3, 1.7881E-1][::-1])
		k_f =  _np.polynomial.Polynomial([-1.7749E-7, -2.7604E-4, 1.8071E-1][::-1])
		k_CHO =  _np.polynomial.Polynomial([-4.3312E-6, 1.3874E-3, 2.0141E-1][::-1])
		k_ash =  _np.polynomial.Polynomial([-2.9069E-6, 1.4011E-3, 3.2962E-1][::-1])
		k_salt =  _np.polynomial.Polynomial([0.574])
		"""
		For salt: 5.704 molal solution at 20C, Riedel L. (1962),
		Thermal Conductivities of Aqueous Solutions of Strong Electrolytes 
		Chem.-1ng.-Technik., 23 (3) P.59 - 64

		Note that previously scisuit.core polynomial was used and the list conforms
		to this (ax^n +... + a0). 
		However, new numpy polynomial uses reverse order and that's why [::-1]
		"""
		
		T=self._m_T

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

		rho_w =  _np.polynomial.Polynomial([-3.7574E-3, 3.1439E-3, 997.18][::-1])
		rho_p =  _np.polynomial.Polynomial([-5.1840E-1, 1329.9][::-1])
		rho_f =  _np.polynomial.Polynomial([-4.1757E-1, 925.59][::-1])
		rho_CHO =  _np.polynomial.Polynomial([-3.1046E-1, 1599.1][::-1])
		rho_ash =  _np.polynomial.Polynomial([-2.8063E-1, 2423.8][::-1])
		rho_salt =  _np.polynomial.Polynomial([2165]) #Wikipedia
		"""
		Note that previously scisuit.core polynomial was used and the list conforms
		to this (ax^n +... + a0). 
		However, new numpy polynomial uses reverse order and that's why [::-1]
		"""
		
		T=self._m_T

		return (self._Water)*rho_w(T) + \
			(self._Protein)*rho_p(T) + \
			(self._Lipid)*rho_f(T) + \
			(self._CHO)*rho_CHO(T) + \
			(self._Ash)*rho_ash(T) + \
			(self._Salt)*rho_salt(T)


	def density(self)->float:
		"""Alias for rho()"""
		return self.rho()


	def aw(self)->float:
		"""
		Returns value of water activity or None \n
		
		## Warning:
		At T>25 C, built-in computation might return None. \n
		Therefore, must be used with caution.
		"""
		aw1 = 0.92
	
		water, CHO, lipid, protein = self._Water, self._CHO, self._Lipid, self._Protein
		ash, salt = self._Ash, self._Salt 

		#note that salt is excluded
		Msolute = CHO + lipid + protein + ash

		#There is virtually no water
		if(water<0.01):
			return 0.01 
	
		#99.99% water
		if(water>0.9999):
			return 1.0
	
		IsElectrolyte = salt>=0.1

		#Non-electrolytes solutions
		if(not IsElectrolyte):
			# Dilute solution, as the total percentage is less than 1%
			if(Msolute<0.01): 
				return 0.99
			
			#almost all CHO
			if(CHO>0.98):
				return 0.70

			#diluted
			if(water>=0.70) :
				aw1 = aw_Raoult(self)

			#solute is 2.5 more times than solvent
			elif(Msolute>=0.70):
				aw1 = aw_Norrish(self)
			
			#most likely a candy
			elif(lipid<0.01 and protein<0.01 and ash<0.01 and water>0.01 and water<0.05 and CHO>0.05): 
				aw1 = aw_MoneyBorn(self)	
			
			else:
				aw1 = aw_FerroFontan_Chirife_Boquet(self)
	
		else:
			aw1 = aw_Raoult(self)
	
		if(self.temperature == 20):
			return aw1

		#average molecular weight
		MWavg = water*18.02 + CHO*180.16 + lipid*92.0944 + protein*89.09 + salt*58.44
	
		T = self.temperature

		self.temperature = 20
		Cp_20 = self.cp()

		self.temperature = T
		Cp_T = self.cp()

		Cp_avg = (Cp_20 + Cp_T) / 2.0	
		Qs = MWavg* Cp_avg*(T - 20.0) #kJ/kg
	
		R = 8.314 #kPa*m^3/kgK

		T += 273.15
		dT = (1/293.15 - 1/T)
	
		aw2 = aw1*_math.exp(Qs/R*dT)
		
		return aw2 if aw2>=0 and aw2<=1 else None
	


	def h(self, T)->float:
		"""
		Computes enthalpy for frozen and unfrozen foods, returns: kJ/kg \n
		T: Initial freezing temperature
		"""	 
		if(not isinstance(T, float)):
			raise TypeError("Initial freezing temperature must be of type float")
			
		return _Enthalpy(self, T)


	def enthalpy(self, T)->float:
		"""Alias for h()"""
		return self.h(T)


	def freezing_T(self):
		"""
		Estimates the initial freezing temperature of a food item \n
		returns in Celcius (None if estimation fails)
		"""
		CHO = self._CHO 
		lipid = self._Lipid 
		water = self._Water 

		Tfreezing = 273.15 # 0.0 Celcius
		
		#assuming it is in a meat group
		if(_math.isclose(CHO, 0.0, abs_tol=1E-5)):
			Tfreezing = 271.18 + 1.47*water

		#fruit or vegetable group
		elif lipid <0.1:
			Tfreezing = 287.56 -49.19*water + 37.07*water**2

		#juice group
		elif water>0.8:
			Tfreezing = 120.47 + 327.35*water - 176.49*water**2

		#no match
		else:
			return None

		#return in Celcius
		return Tfreezing - 273.15

	


	def x_ice(self, T:float)->float:
		"""
		Finds the fraction of ice \n
		T: Initial freezing temperature
		"""
		Tfood = self._m_T

		"""
		if food temperature greater than initial freezing temperature
		then no ice can exist
		"""
		if(Tfood > T):
			return 0.0

		Tdiff = T -Tfood + 1

		assert Tdiff>0, "Are you sure food's temperature is smaller than freezing temperature?"

		#Tchigeov's (1979) equation (Eq #5 in ASHRAE manual)
		xice = 1.105*self._Water / (1 + 0.7138/_math.log(Tdiff))

		return xice
	

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
			assert HasIntersection(self, f), "List has food item with no common ingredient with the target"
		
		Ingredients = self.getIngredients()
		NCols = len(Ingredients) + 1

		for key, value in Ingredients.items():
			row = []
			for f in Foods:
				ing = f.getIngredients()
				val = 0.0
				if(ing.get(key)!= None):
					val = ing[key]/100
				row.append(val)
			
			assert len(row) == NCols, "Malformed matrix"
			A.append(row)
			b.append(value/100*self.weight)

		#solve Ax=b
		return _np.linalg.solve(_np.asfarray(A), _np.asfarray(b))



	def getIngredients(self)->dict:
		retDict = dict()
		for k, v in self.__Ingredients.items():
			if(v>0):
				retDict[k] = v
		return retDict
	

	def normalize(self):
		"""
		sets the weight to 1.0
		"""
		self._m_Weight = 1.0


	@property
	def temperature(self):
		"""in Celcius, same as property T"""
		pass

	@temperature.setter
	def temperature(self, T):
		assert T+273.15 >= 0, "Temperature > 0 Kelvin expected"
		self._m_T = T

	@temperature.getter
	def temperature(self)->float:
		return self._m_T
	
	@property
	def T(self):
		"""in Celcius, same as property temperature"""
		pass

	@T.setter
	def T(self, T):
		assert T+273.15 >= 0, "Temperature > 0 Kelvin expected"
		self._m_T = T

	@T.getter
	def T(self)->float:
		return self._m_T



	@property
	def weight(self):
		""" unit weight, NOT recommended to set the weight externally """
		pass

	@weight.setter
	def weight(self, weight:float):
		self._m_Weight=weight
	
	@weight.getter
	def weight(self)->float:
		return self._m_Weight


	@property
	def Water(self)->float:
		return self._Water
	
	@property
	def CHO(self)->float:
		return self._CHO

	@property
	def Lipid(self)->float:
		return self._Lipid

	@property
	def Protein(self)->float:
		return self._Protein

	@property
	def Ash(self)->float:
		return self._Ash

	@property
	def Salt(self)->float:
		return self._Salt



	#similar to mixing of two food items
	def __add__(self, foodB:Food)->Food:
		ma, mb = self.weight,  foodB.weight
		Ta, Tb = self.temperature, foodB.temperature 
		cpa, cpb = self.cp(), foodB.cp()

		water = ma*self.Water + mb*foodB.Water
		CHO = ma*self.CHO + mb*foodB.CHO
		lipid = ma*self.Lipid + mb*foodB.Lipid
		protein = ma*self.Protein + mb*foodB.Protein
		ash = ma*self.Ash + mb* foodB.Ash
		salt = ma*self.Salt + mb* foodB.Salt

		sum = water + CHO + lipid + protein + ash + salt

		retFood = Food(water=water/sum, CHO=CHO/sum, lipid=lipid/sum, protein=protein/sum, ash=ash/sum, salt=salt/sum)
		retFood.weight= ma + mb
	
		"""
		if the other food's temperature is negligibly different 
		then mixtures temperature is one of the food items' temperature
		"""
		if(_math.isclose(Ta, Tb, rel_tol=1E-5)):
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

		fA, fB = self.getIngredients(), foodB.getIngredients()
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
		if(not isinstance(elem, _numbers.Number)):
			raise TypeError("Foods can only be multiplied by numbers")

		newFood = self.getIngredients()
		retFood = Food(**newFood)

		retFood.weight = self.weight*elem

		return retFood




	def __rmul__(self, elem:float)->Food:
		if(not isinstance(elem, _numbers.Number)):
			raise TypeError("Foods can only be multiplied by numbers")
	 
		newFood = self.getIngredients()
		retFood = Food(**newFood)

		retFood.weight = self.weight*elem

		return retFood

	

	def __str__(self):
		retStr=""

		retStr += "Weight (unit weight)=" + str(round(self.weight, 2)) +"\n"

		retStr += "Temperature (C)=" + str(round(self.temperature, 2)) +"\n"

		if(self._Water>0): 
			retStr += "Water (%)=" + str(round(self._Water*100, 2)) +"\n" 

		if(self._Protein>0): 
			retStr += "Protein (%)=" + str(round(self._Protein*100, 2)) +"\n" 
		
		if(self._CHO>0): 
			retStr += "CHO (%)=" + str(round(self._CHO*100, 2)) +"\n" 
		
		if(self._Lipid>0): 
			retStr += "Lipid (%)=" + str(round(self._Lipid*100, 2)) +"\n"

		if(self._Ash>0): 
			retStr += "Ash (%)=" + str(round(self._Ash*100, 2)) +"\n" 

		if(self._Salt>0): 
			retStr += "Salt (%)=" + str(round(self._Salt*100)) +"\n" 
		
		aw = self.aw()
		if(aw != None):
			retStr +="aw=" + str(round(aw, 3)) + "\n"	

		return retStr


	
	def __eq__(self, foodB:Food)->bool:

		if(not isinstance(foodB, Food)):
			return False

		fA, fB = self.getIngredients(), foodB.getIngredients()

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
			if(not _math.isclose(v, fB[k], rel_tol=1E-5)):
				return False
			
		return True



"""
if __name__=='__main__':
	f1 = Food(CHO=30, water=70)
	f2 = Food(protein=20, water=70, CHO=10)
	print(f1)
	print(f2)
	print(f1+f2)
"""