import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


from scisuit.eng import psychrometry

#linear combination
result = psychrometry(P=101, Tdb=35, Twb=20)

#testing new solver method
result2 = psychrometry(V=result.V, Twb=result.Twb, Tdp=result.Tdp)

#all of the properties
print(result)
print(result2)

