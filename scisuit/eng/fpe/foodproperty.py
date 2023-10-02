import math as _math

class Food:
	pass



def ComputeAw_T(food:Food, aw1:float)->float|None:
	"""
	Computes aw at a different temperatures
	
	food: Food material
	aw1: water activity of food at reference temperature (generally around 20C)
	T2: the temperature at which water activity will be computed
	"""
	Tref = 20
	if _math.isclose(food.T, Tref, abs_tol=1.0):
		return aw1

	#save the actual temperature
	T = food.T

	food.T = Tref
	Cp_20 = food.cp()

	#restore the actual temperature
	food.T = T
	Cp_T = food.cp()

	Cp_avg = (Cp_20 + Cp_T) / 2.0	
	Qs = food.molecularweight()* Cp_avg*(T - 20.0) #kJ/kg

	R = 8.314 #kPa*m^3/kgK

	T += 273.15
	dT = 1/293.15 - 1/T

	aw2 = aw1*_math.exp(Qs/R*dT)
	
	return aw2 if aw2>=0 and aw2<=1 else None



#-----------------------------------------------------------------------------


class Aw():
	def __init__(self, food:Food) -> None:
		self._food = food


	def FerroFontan_Chirife_Boquet(self)->float:
		"""
		CHO is considered as fructose \n
		protein is considered as alanine \n
		lipid is considered as glycerol
		"""
		MW_CHO = 180.16
		MW_LIPID = 92.0944
		MW_PROTEIN = 89.09

		fd = self._food

		NCHO, NLipid, NProtein = fd.cho/MW_CHO, fd.lipid/ MW_LIPID, fd.protein/MW_PROTEIN
		
		#number of moles of water
		N_w = fd.water/18.02

		#solute
		N_slt = NCHO + NLipid + NProtein

		Solute = 1 - fd.water
		C_cho, C_Lipid, C_Protein = fd.cho/Solute, fd.lipid/Solute, fd.protein/Solute

		Mt = _math.sqrt(C_cho/MW_CHO + C_Lipid/MW_LIPID + C_Protein/MW_PROTEIN)

		# Norrish equation K values using Ferro-Chirife-Boquet equation
		Km = C_cho*(Mt/MW_CHO)*(-2.15) +C_Lipid*(Mt/MW_LIPID)*(-1.16) + C_Protein*(Mt/MW_PROTEIN)*(-2.52) 
		
		# Mole fraction of solute
		X_slt = N_slt/(N_slt + N_w) 

		# Mole fraction of water
		XWater = N_w/(N_slt + N_w) 

		aw = XWater*_math.exp(Km*X_slt**2)

		return aw



	def Norrish(self)->float:
		"""Norrish equation"""
		
		f = self._food

		#CHO is considered as fructose
		N_cho = f.cho/180.16 
		
		#lipid is considered as glycerol
		N_l = f.lipid/ 92.0944 
		
		#protein is considered as alanine
		N_p = f.protein/89.09 

		#water
		N_w = f.water / 18

		#total
		N_tot = N_cho + N_l + N_p + N_w

		#X_l: lipid, X_p: protein, X_w: water
		X_cho, X_l, X_p, X_w = N_cho/N_tot, N_l/N_tot, N_p/N_tot, N_w/N_tot

		
		# Norrish equation K values using Ferro-Chirife-Boquet equation
		SumSq = -(2.15)*X_cho**2 - (1.16)*X_l**2 - (2.52)*X_p**2
		SumX2 = X_cho**2 + X_l**2 + X_p**2
		
		rhs = _math.log(X_w) + SumSq/SumX2*(1-X_w)**2

		return _math.exp(rhs)



	#mostly used in confectionaries
	def MoneyBorn(self)->float:
		f = self._food

		# amount of CHO in 100 g water (equation considers thus way) 
		W = 100*f.cho/f.water 
		
		#CHO is considered as fructose
		N_cho = W/180.16 
		
		return 1.0/(1.0 + 0.27*N_cho)



	def Raoult(self)->float:
		#prediction using Raoult's law
		#all in percentages

		f = self._food

		x_w = f.water
		xCHO =  f.cho
		x_l = f.lipid
		x_p =  f.protein

		#solute
		x_slt = xCHO + x_l + x_p + f.ash

		#average molecular weight
		MW_slt = (xCHO/x_slt)*180.16 + (x_l/x_slt)*92.0944 + (x_p/x_slt)*89.09 if x_slt>0 else 1
			
		MW_w=18 #molecular weight of water
		MW_nacl = 58.44

		temp1 = x_w + (MW_w/MW_slt)*x_slt + 2*(MW_w/MW_nacl)*f.salt
		return x_w/temp1





""" ------------------------------------------------------------------------------- """

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
