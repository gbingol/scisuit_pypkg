import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

from scisuit.eng.refrigerants import Refrigerant

r = Refrigerant.SR12()
print(r.hf>20)