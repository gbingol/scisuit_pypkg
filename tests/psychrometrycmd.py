from scisuit.eng import psychrometry

#linear combination
result = psychrometry(P=101, Tdb=70, Twb=40)

#testing new solver method
result2 = psychrometry(RH=result.RH, H=result.H, P=result.P)

#all of the properties
print(result)
print(result2)

