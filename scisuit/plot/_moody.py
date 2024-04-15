import math

from ..roots import brentq
from ._charts import canvas, xscale, yscale
from .gdi import marker, line, curve, text
from ..util import NiceNumbers


def _Colebrook(f, Re, E_D):
	#inside log
	temp1 = E_D/3.7 + 2.51/(Re*math.sqrt(f)) 
	temp2 = 2.0* math.log10(temp1) 

	return 1/math.sqrt(f) + temp2

def _vonKarman(f, E_D):
	temp = 2.0* math.log10(E_D/3.7) 
	return 1/math.sqrt(f) + temp



def moody():
	Reynolds = [1E3, 1E7] #Reynolds number
	FricFact = [0.01, 0.08] #friction factor

	canvas(x=Reynolds, y=FricFact)
	xscale("log")
	yscale("log")

	#laminar flow 0<Re<2300
	fD = lambda Re: 64.0/Re
	p1 = (1000, fD(1000))
	p2 = (2300, fD(2300))
	line(p1=p1, p2=p2, lw=2, ls="--", ec="#FF0000")

	#Turbulent Region - Re>=4000
	Re = [4000, 6000, 9000, 12E3, 20E3, 30E3, 60E3, 120E3, 250E3, 1E6, 5E6]

	e_d = [5E-5, 1E-4, 5E-4, 1E-3,2.5E-3, 5E-3, 0.01, 0.02, 0.03, 0.04, 0.05]

	for _e_d in e_d:
		x, y = [], []
		for re in Re:
			_cb = lambda f: _Colebrook(f, re, _e_d)
			friction, _ = brentq(_cb, a=0.001, b=0.08)
			x.append(re)
			y.append(friction)

		text(xy=(re, friction), label=str(_e_d), anchor="cl")
		curve(x, y, lw=2, ec="#A52A2A")

	
		
