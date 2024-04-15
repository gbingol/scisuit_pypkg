import math

from ..roots import brentq
from ._charts import canvas, xscale, yscale
from .gdi import line, curve, text, rect


def _Colebrook(f, Re, E_D):
	#inside log
	temp1 = E_D/3.7 + 2.51/(Re*math.sqrt(f)) 
	temp2 = 2.0* math.log10(temp1) 

	return 1/math.sqrt(f) + temp2



def _TurbulenceOnset(E_D):	
	"""
	compute friction factor
	A modified version of Colebrook's equation for large Re
	"""
	def _vonKarman(E_D):
		f = -2.0* math.log10(E_D/3.7) 
		return (1/f)**2
	
	"""
	compute Reynolds number
	Transactions of the ASME, 66 (8): 671-684 (Page: 676)
	"""
	def _Reynolds(f):
		return 1/math.sqrt(f)*200/E_D
	
	f = _vonKarman(E_D)
	Re = _Reynolds(f)
	return Re, f




def moody():
	Reynolds = [1E3, 1E7] #Reynolds number
	FricFact = [0.01, 0.08] #friction factor

	canvas(x=Reynolds, y=FricFact)
	xscale("log")
	yscale("log")

	"""
	laminar flow 0<Re<2300
	"""
	fD = lambda Re: 64.0/Re
	p1 = (1000, fD(1000))
	p2 = (2300, fD(2300))
	line(p1=p1, p2=p2, lw=2, ls="--", ec="#FF0000")


	text(xy=p2, label="Laminar\n f=64/Re", hanchor="c")

	"""
	transition region 2300<Re<4000
	btmleft: x (onset of transition), y(roughly 64/Re)
	rectangle's width = 4000-2300=1700, height=0.08-0.03
	"""
	btmleft = (2300, 0.03)
	rect(xy=btmleft, width=1700, height=0.05, hatch="/", ls="--", fc="#808080")

	"""
	Turbulent Region - Re>=4000
	"""
	Re = [4000, 6000, 9000, 12E3, 20E3, 30E3, 60E3, 120E3, 250E3, 1E6, 5E6]

	e_d = [5E-5, 1E-4, 5E-4, 1E-3,2.5E-3, 5E-3, 0.01, 0.02, 0.03, 0.04, 0.05]

	TurbulenceLine = []
	for _e_d in e_d:
		x, y = [], []
		TurbulenceLine.append(_TurbulenceOnset(_e_d))
		for re in Re:
			_cb = lambda f: _Colebrook(f, re, _e_d)
			friction, _ = brentq(_cb, a=0.001, b=0.08)
			x.append(re)
			y.append(friction)

		text(xy=(re, friction), label=str(_e_d), vanchor="c")
		curve(x, y, lw=2, ec="#A52A2A")


	"""
	fully rough turbulent flow line
	"""
	_turbulence = list(zip(*TurbulenceLine))
	curve(x=_turbulence[0], y=_turbulence[1], lw=2, ls="--")
	
		
