import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.eng.fpe as fpe

milk = fpe.Food(water=88.13, protein=3.15, cho=4.8, lipid=3.25, ash=0.67)
print(milk)

#different percentages of same ingredients
f1= fpe.Food (water =80, cho=20)
f2= fpe.Food (water =60, cho=40)

print(f1 == f2)

f = fpe.Food (water=40, protein=20)
print(f)
f2= fpe.Food (water =60, cho=40)

