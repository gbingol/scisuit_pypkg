import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


from scisuit.eng.fpe import Food, FoodType

milk = Food(water=0.8813, protein=0.0315, cho=0.0480, lipid=0.0325, ash=0.0067)
print(milk)

#different percentages of same ingredients
f1= Food (water =80, cho=20)
f2= Food (water =60, cho=40)

print(f1 == f2)

f1= Food (water =80, protein=20)
f2= Food (water =60, cho=40)

print(f1 == f2)