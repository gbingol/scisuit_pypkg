import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


from scisuit.eng import psychrometry

res1 = psychrometry(P=101, Tdb=30, Twb=20)
print(res1)

def h():
    return None

def prt():
    return h()

def h():
    return "hi there"

print(prt())