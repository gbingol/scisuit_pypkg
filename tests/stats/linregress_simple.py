from scisuit.stats import linregress

x = [4.3, 4.6, 5.2, 5.3, 5.5, 5.7, 6.1, 6.3, 6.8, 7.5]
y = [7.7, 5.2, 7.9, 5.8, 7.2, 7, 5.3, 6.8, 6.6, 4.7]

result = linregress(yobs=y, factor=x)
print(result)