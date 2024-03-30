import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.eng.fpe as fpe
import scisuit.eng as eng

milk = fpe.Food(water=88.13, protein=3.15, cho=4.80, lipid=3.25, ash=0.67)

milk.T = 50
print(f"cp={milk.cp()}")
print(f"rho={milk.rho()}")
print(f"k={milk.k()}")

