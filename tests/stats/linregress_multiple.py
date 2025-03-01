from scisuit.stats import linregress

#input values
temperature = [80, 93, 100, 82, 90, 99, 81, 96, 94, 93, 97, 95, 100, 85, 86, 87]
feedrate = [8, 9, 10, 12, 11, 8, 8, 10, 12, 11, 13, 11, 8, 12, 9, 12]
viscosity = [2256, 2340, 2426, 2293, 2330, 2368, 2250, 2409, 2364, 2379, 2440, 2364, 2404, 2317, 2309, 2328]

#note the order of input to factor
result = linregress(yobs=viscosity, factor=[temperature, feedrate])
print(result)