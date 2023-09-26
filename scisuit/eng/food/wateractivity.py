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
		MW_Lipid = 92.0944
		MW_Protein = 89.09

		food = self._food

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



	def Norrish(self)->float:
		"""Norrish equation"""
		
		food = self._food

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
	def MoneyBorn(self)->float:
		food = self._food

		# amount of CHO in 100 g water (equation considers thus way) 
		WeightCHO = 100*food.CHO/food.Water 
		
		#CHO is considered as fructose
		NCHO = WeightCHO/180.16 
		
		return 1.0/(1.0 + 0.27*NCHO)


	def Raoult(self)->float:
		#prediction using Raoult's law
		#all in percentages

		food = self._food

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