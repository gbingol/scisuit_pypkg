from scisuit.eng import psychrometry

#linear combination
result = psychrometry(P=101, Tdb=20, Twb=15)
print(result)


#result2 = psychrometry(Twb=result.Twb, H=result.H, Tdp=result.Tdp)
#result2 = psychrometry(V=result.V, Twb=result.Twb, Tdp=result.Tdp)

result2 = psychrometry(V=0.8, RH=60, P=101)

print(result2)