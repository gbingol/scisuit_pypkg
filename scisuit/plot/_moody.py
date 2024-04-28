import math
from typing import Iterable

from ..roots import brentq
from ._charts import canvas, title, xlabel, xscale, ylabel, yscale
from .gdi import arrow, curve, line, rect, text


def _Colebrook(f, Re, E_D):
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



def moody(
		Re:Iterable = [1E3, 1E7],
		friction:Iterable = [0.01, 0.09],
		showlaminar = True,
		showtransition = True,
		showturbulent = True):
	"""
	`Re:` Reynolds number range
	`friction:`  Friction factor range
	`showlaminar:` show laminar line and related info
	`showtransition:` show transition region and related info
	`showturbulent:` show fully turbulent line and related info
	"""
	assert isinstance(Re, Iterable), "Re must be iterable"
	assert len(Re)==2, "Re must have length 2"

	assert isinstance(friction, Iterable), "friction must be iterable"
	assert len(friction)==2, "friction must have length 2"

	canvas(
		x=(float(Re[0]), float(Re[1])), 
		y=(float(friction[0]), float(friction[1])))
	xscale("log")
	yscale("log")

	"""
	laminar flow 0<Re<2300
	"""
	if showlaminar:
		fD = lambda _Re: 64.0/_Re
		p1 = (1000, fD(1000))
		p2 = (2300, fD(2300))
		line(p1=p1, p2=p2, lw=2, ls="--", ec="#FF0000", label="laminar")
		text(xy=p2, label="Laminar Flow\nf = 64/Re", hanchor="c")

	"""
	transition region 2300<Re<4000
	btmleft: x (onset of transition), y(roughly 64/Re)
	rectangle's width = 4000-2300=1700, height=0.08-0.03
	"""
	if showtransition:
		btmleft = (2300, 0.03)
		idrect = rect(xy=btmleft, width=1700, height=0.05, hatch="solid", alpha=0.5, ls="--", fc="#808080", label="transition")
		idtext = text(xy=(3300, 0.06), label="Transition Region", rotation=-90, labelcolor="#A52A2A")

	"""
	Turbulent Region - Re>=4000
	"""
	Re_Turbulent = [4000, 6000, 9000, 12E3, 20E3, 30E3, 60E3, 120E3, 250E3, 1E6, 5E6]
	e_d = [5E-5, 1E-4, 5E-4, 1E-3,2.5E-3, 5E-3, 0.01, 0.02, 0.03, 0.04, 0.05]

	TurbulenceLine = []
	for _e_d in e_d:
		x, y = [], []
		TurbulenceLine.append(_TurbulenceOnset(_e_d))
		for _Re in Re_Turbulent:
			_cb = lambda f: _Colebrook(f, _Re, _e_d)
			friction, _ = brentq(_cb, a=0.001, b=0.08)
			x.append(_Re)
			y.append(friction)

		text(xy=(_Re, friction), label=str(_e_d), vanchor="c")
		curve(x, y, lw=2, ec="#A52A2A", label=str(_e_d))

	"""
	fully rough turbulent flow line
	E/D=0.06 appended so that the dashed line will be slightly above E/D=0.05 line
	"""
	if showturbulent:
		TurbulenceLine.append(_TurbulenceOnset(0.06))
		_turbulence = list(zip(*TurbulenceLine))
		curve(x=_turbulence[0], y=_turbulence[1], lw=2, ls="--")
		
		midpoint = int(len(TurbulenceLine)/2)
		xx, yy=_turbulence[0][midpoint], _turbulence[1][midpoint]
		_p1 = (15E3, 0.015)
		arrow(p1=_p1, p2=(xx,yy), lw=2, length=0.05, label="arrow")
		text(xy=_p1, label="Complete Turbulence", hanchor="c")

	xlabel("Reynolds Number")
	ylabel("Friction Factor")
	title("Moody Diagram")
