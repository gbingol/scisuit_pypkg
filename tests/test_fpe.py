import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.eng.fpe as fpe
import scisuit.eng as eng
import scisuit.plot as plt
from math import pi, exp


#compute Nussel number
def Nu(Re, Pr):
	C, m = 0,0
	if 0.4 <= Re < 4:
		C , m= 0.989, 0.330
	elif 4 <= Re < 40:
		C, m = 0.911, 0.385
	elif 40 <= Re < 4000:
		C, m = 0.683, 0.466

	return C*Re**m*Pr**(1/3)



grape = fpe.Food(water=80, cho=20)

Tair, T0_grape = 58, 26 #C
V = 0.6  #m/s
D, L = 1.9 /100,  29.7/100 #m

#critical length
Lc = D / 2 

#film temperature
Tf = (Tair + T0_grape)/2 

air = eng.Air(T=Tf+273.15)

Re = (air.rho()*V*D) / air.mu()

Nu_ = Nu(Re=Re, Pr=air.Pr())
h = Nu_*air.k()/Lc

""" Lumped Heat Capacity Analysis """
Volume = pi*(D**2/4)*L
SurfaceArea =  2*pi*D**2/4 + pi*D*L

Lc_lumped = Volume/SurfaceArea #critical length in lumped analysis

Bi = h*Lc_lumped/grape.k()
b = h /(grape.rho()* grape.cp()*1000*Lc_lumped)

# 22 minutes, sample every minute
t_sim = range(0, 23) 
T_sim = [exp(-b*t*60)*(T0_grape - Tair) + Tair for t in t_sim]

t_exp = [0, 1.007, 2.006, 3.01, 4.001, 5.009, 6.005, 7.007, 8.005, 9.002, 10.004, 11.004, 
	12.005, 13.008, 14.005, 15.002, 16.001, 17.008, 18.005, 19.005, 20.007, 21.005, 
	22.002, 22.104, 22.206, 22.309, 22.401, 22.506]

T_exp = [26.268, 28.933, 31.393, 33.828, 36.028, 38.173, 40.093, 41.778, 43.443, 44.953, 46.208, 
	47.438, 48.498, 49.403, 50.308, 51.113, 51.673, 52.248, 52.873, 53.343, 53.748, 
	54.218, 54.593, 54.573, 54.588, 54.653, 54.713, 54.733]

plt.scatter(x=t_sim, y=T_sim, label="simulation")
plt.scatter(x=t_exp, y=T_exp, label="experimental")
plt.legend()
plt.show()


# detailed definition of CHO 
carbs = fpe.CHO(glucose = 40, fructose = 60) 

#food made of water and CHO (glucose + fructose)
food = fpe.Food(CHO = 40* carbs, water = 60)