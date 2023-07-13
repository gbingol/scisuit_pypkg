import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


from scisuit.eng import Food

f1= Food (water =80, CHO=20)
f2= Food (water =60, CHO=10, protein = 30)

f1.T = 10 #at 10°C
f2.T = 25 #at 25°C

"""create a mixture of equal weights
mass and energy balances performed automatically"""
f3 = f1 + f2

print(f3)

"""
milk = Food(
    water=88.13, 
    protein=3.15, 
    CHO=4.80, 
    lipid=3.25, 
    ash=0.67)

water = Food(water=100)

#removal of 87% water from milk
powder = milk - 0.87*water 

print(milk)

print("------------ \n")

print(powder)

"""
