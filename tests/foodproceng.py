import scisuit.eng.fpe as fpe

milk = fpe.Food(water=88.13, protein=3.15, cho=4.80, lipid=3.25, ash=0.67)

milk.T = 30
print(f"cp={milk.cp()}")
print(f"rho={milk.rho()}")
print(f"k={milk.k()}")
print(f"aw={milk.aw()}")

for k, v in milk:
    print(k, v)

print(list(milk))