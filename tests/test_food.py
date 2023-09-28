import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


from scisuit.eng.fpe import Food, FoodType


#defined and constructed
milk = Food(water=88.13, protein=3.15, cho=4.80, lipid=3.25, ash=0.67, categ=FoodType.dairy)
print(milk)

#different percentages of same ingredients
f1= Food (water =80, cho=20)
f2= Food (water =60, cho=40)

print(f1 == f2)

f1= Food (water =80, protein=20)
f2= Food (water =60, cho=40)

print(f1 == f2)