from scisuit.eng import psychrometry

#linear combination
result = psychrometry(P=101, Tdb=20, Twb=15)
print(result)


#result2 = psychrometry(Twb=result.Twb, H=result.H, Tdp=result.Tdp)
#result2 = psychrometry(V=result.V, Twb=result.Twb, Tdp=result.Tdp)

#ValueError: W < 0.0
result2 = psychrometry(V=result.V, RH=result.RH, Tdb=result.Tdb)

print(result2)