import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit.eng.fluids_dbase import ThermoPhysical, SaturatedRefrigerant

f = ThermoPhysical("water")
res = f.search("T", 20)
print(res)

ref = SaturatedRefrigerant("water")
res = ref.search("T", 30)
print(res)