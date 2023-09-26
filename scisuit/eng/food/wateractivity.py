import math as _math

class Food:
	pass


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

		food = self._food

		NCHO, NLipid, NProtein = food.cho/MW_CHO, food.lipid/ MW_LIPID, food.protein/MW_PROTEIN
		NWater = food.water/18.02
		Nsolute = NCHO + NLipid + NProtein

		Solute = 1 - food.water
		C_CHO, C_Lipid, C_Protein = food.cho/Solute, food.lipid/Solute, food.protein/Solute

		Mt= _math.sqrt(C_CHO/MW_CHO + C_Lipid/MW_LIPID + C_Protein/MW_PROTEIN)

		# Norrish equation K values using Ferro-Chirife-Boquet equation
		Km = C_CHO*(Mt/MW_CHO)*(-2.15) +C_Lipid*(Mt/MW_LIPID)*(-1.16) + C_Protein*(Mt/MW_PROTEIN)*(-2.52) 
		
		# Mole fraction of solute
		XSolute = Nsolute/(Nsolute + NWater) 

		# Mole fraction of water
		XWater = NWater/(Nsolute + NWater) 

		aw = XWater*_math.exp(Km*XSolute**2)

		return aw



	def Norrish(self)->float:
		"""Norrish equation"""
		
		f = self._food

		#CHO is considered as fructose
		NCHO = f.cho/180.16 
		
		#lipid is considered as glycerol
		NLipid = f.lipid/ 92.0944 
		
		#protein is considered as alanine
		NProtein = f.protein/89.09 
		Nsolute = NCHO + NLipid + NProtein
		NWater = f.water / 18
		NTotal = NCHO + NLipid + NProtein + NWater

		XCHO, XLipid, XProtein, XWater = NCHO/NTotal, NLipid/NTotal, NProtein/NTotal, NWater/NTotal

		
		# Norrish equation K values using Ferro-Chirife-Boquet equation
		SumSq = -(2.15)*XCHO**2 - (1.16)*XLipid**2 - (2.52)*XProtein**2
		SumX2 = XCHO**2 + XLipid**2 + XProtein**2
		
		RHS = _math.log(XWater) + SumSq/SumX2*(1-XWater)**2

		return _math.exp(RHS)



	#mostly used in confectionaries
	def MoneyBorn(self)->float:
		f = self._food

		# amount of CHO in 100 g water (equation considers thus way) 
		W = 100*f.cho/f.water 
		
		#CHO is considered as fructose
		NCHO = W/180.16 
		
		return 1.0/(1.0 + 0.27*NCHO)


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
			
		MW_Water=18
		MW_NaCl = 58.44

		temp1 = x_w + (MW_Water/MW_slt)*x_slt + 2*(MW_Water/MW_NaCl)*f.salt
		return x_w/temp1