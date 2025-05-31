from scisuit.stats import test_wilcox

data1 = {
	"x":[7.8, 6.6, 6.5, 7.4, 7.3, 7., 6.4, 7.1, 6.7, 7.6, 6.8], 
	"md":6.5, "confint":False}

data2 = {
	"x":[24, 28, 28, 31, 32, 33, 38, 39, 41, 43, 48, 49, 49, 51, 52, 56, 56, 58, 62, 63],
	"md": 40}


result = test_wilcox(**data1)
print(result)