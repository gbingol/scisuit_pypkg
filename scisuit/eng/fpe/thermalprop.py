import math as _math

class Food:
	pass


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


	def Heldman(self):
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
