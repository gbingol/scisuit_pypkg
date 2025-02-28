from scisuit.stats import test_sign, dbinom



x = [7.8, 6.6, 6.5, 7.4, 7.3, 7., 6.4, 7.1, 6.7, 7.6, 6.8]
result = test_sign(x=x, md=6.5)
print(result)