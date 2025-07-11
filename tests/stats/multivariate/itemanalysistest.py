from scisuit.stats import cronbach
from scisuit.stats.multivariate import adjtotalcorrel, squaredmultcorrel

Items = [ 
    [5,2,3,1,3,3,4,3,3,4,1,2,5,5,4,4,2,2,3,2,5, 3,3,2,3,2,5,3,2,5,2,4,5,5,2,3,2,1,1,4,3,4,3,5,3,3,1,5,4,4,], 
    [5,2,2,1,2,3,4,3,2,4,1,2,4,5,4,3,1,1,3,2,5,3,2,1,3,2,5,1,1,5,2,3,5,5,3,2,1,1,1,4,3,3,3,5,3,2,2,4,4,4,], 
    [5,1,4,1,2,3,4,3,3,4,2,2,4,5,5,4,1,1,3,1,4,2,3,2,3,2,5,1,1,5,1,4,4,4,3,2,1,2,2,4,3, 4,3,5,3,3,1,5,4,3,]]

result = cronbach(Items, [])
print(result)

print(adjtotalcorrel(Items))
print(squaredmultcorrel(Items))