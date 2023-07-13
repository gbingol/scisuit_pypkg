import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


from scisuit.eng import psychrometry

result = psychrometry(P=101, Tdb=30, Twb=20)

#all of the properties
print(result)

print("----------------------- \n")

#an individual property (enthalpy)
print("h=" + str(result.H))