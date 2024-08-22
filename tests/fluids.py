import sys, os
import numpy as np
import pathlib

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, pathlib.Path(__file__).parent.parent) 


from scisuit.eng import Refrigerant


def water():
	from scisuit.eng import Water

	#temperature in Celcius
	water = Water(25)

	print(f"Density (kg/m3): {water.density()}")
	print(f"Viscosity (Pa*s): {water.viscosity()}")


def dryair():
	from scisuit.eng import Air

	#temperature Kelvin
	air = Air(T=300)

	print(f"Density (kg/m3): {air.density()}")
	print(f"Viscosity (Pa*s): {air.viscosity()}")


r = Refrigerant().SR12()
rng = np.where(np.logical_and(r.hf>20, r.hf<50))
print(list(map(lambda i: r.hf[i], rng)))


water()
dryair()