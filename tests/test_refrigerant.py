import sys, os
import pprint

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


from scisuit.eng import SaturatedRefrigerant

#saturated properties of water
fl = SaturatedRefrigerant("water")

#search properties for T=10°C
result = fl.search("T", 10)

#print dictionary containing properties
pprint.pprint(result)

print("\n ----------- \n")

#print enthalpy
print("hg=" + str(result["hg"]))