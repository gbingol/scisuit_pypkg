import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.eng.fpe as fpe

milk = fpe.Food(water=88.13, protein=3.15, cho=4.80, lipid=3.25, ash=0.67)
water = fpe.Food(water=100)

#removal of 87% water from milk (Food - Food = Food)
powder = milk - 0.87*water
print(powder)

#convert general powder into a dairy powder
dairy_powder = fpe.Dairy(**powder.ingredients())
print(dairy_powder)