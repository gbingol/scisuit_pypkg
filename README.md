## scisuit

All-in-one, high performance, scientific computing and visualization library designed with engineers
in mind..


&nbsp;




## Plot Library

Interactive charts (Bar, Box-Whisker, Bubble, Direction Field, Histogram, Moody, Psychrometry, 
QQnorm, QQplot, Quiver, Scatter). 


A simple scatter chart example:


```python
import numpy as np
import scisuit.plot as plt 

x = np.arange(1, 6)
y = x**2 - 2*x + 5

plt.scatter(x=x, y=y)
plt.show()
```

See in action on YouTube: [Scatter Chart](https://youtu.be/g3aJyNOOAn8), [Psychrometric Chart](https://youtu.be/Uv4npLsV1sY)

&nbsp;
&nbsp;


## Engineering Library

Designed mostly for process engineers.

### Examples

**1. Psychrometry:**

Computation of properties of humid-air.

```python
from scisuit.eng import psychrometry

r = psychrometry(P=101, Tdb=30, Twb=20)

#all of the properties
print(r)
```
```
P=101.0 kPa,
Tdb=30.0 C
Twb=20.0 C
Tdp=14.17 C
H=57.06 kJ/kg da
RH=39.82 %
W=0.0106 kg/kg da
V=0.876 m3/kg da
```


&nbsp;

**2. Food:**

A rich class for not only computation of food properties but also
to perform food arithmetic.

```python
import scisuit.eng as eng

milk = eng.Food(water=88.13, protein=3.15, cho=4.80, lipid=3.25, ash=0.67)
water = eng.Food(water=100)

#removal of 87% water from milk
powder = milk - 0.87*water 
print(powder)
```

```
Type = Food
Weight (unit weight) = 0.13
Temperature (C) = 20.0
water (%) = 8.69
cho (%) = 36.92
protein (%) = 24.23
lipid (%) = 25.0
ash (%) = 5.15
aw = 0.194
```


&nbsp;
&nbsp;


## Statistics Library

Statistical tests & distributions.

```python
from scisuit.stats import linregress

#input values
temperature = [80, 93, 100, 82, 90, 99, 81, 96, 94, 93, 97, 95, 100, 85, 86, 87]
feedrate = [8, 9, 10, 12, 11, 8, 8, 10, 12, 11, 13, 11, 8, 12, 9, 12]
viscosity = [2256, 2340, 2426, 2293, 2330, 2368, 2250, 2409, 2364, 2379, 2440, 2364, 2404, 2317, 2309, 2328]

#note the order of input to factor
result = linregress(yobs=viscosity, factor=[temperature, feedrate])
print(result)

#Output
Multiple Linear Regression  
F=82.5, p-value=4.0997e-08, R2=0.93

Predictor        Coeff        StdError         T             p-value
X0               1566.078         61.59       25.43       9.504e-14
X1               7.621            0.62        12.32       3.002e-09
X2               8.585            2.44        3.52        3.092e-03
```


&nbsp;
&nbsp;


## Numerics Library

Libraries for solving ODE, root finding, fitting, integration...

```python
from scisuit.roots import bisect, brentq, itp

args = {"f":lambda x: x**2-5, "a":0, "b": 4} 

for func in [bisect, brentq, itp]:
    print(func(**args))
```

```
Bisection using brute-force method 
Root=2.23607, Error=3.35e-06 (18 iterations).

Brent's method (inverse quadratic interpolation)
Root=2.23607, (7 iterations).

ITP method
Root=2.23607, Error=3.43e-07 (7 iterations).
```