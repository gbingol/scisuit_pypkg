import scisuit.eng as fpe
f = fpe.Food(water=96.6, cho=0, protein=2.26, lipid=0.81, ash=0.74, salt=0)
f.T = 20

f2 = fpe.Food(water=85.7, cho=9.52, protein=2.38, lipid=1.59, ash=0.8, salt=0)
f2.T = 25

print(f+f2)