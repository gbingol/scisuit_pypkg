from ._charts import canvas, xscale
from .gdi import marker, line, curve
from ..util import NiceNumbers


def moody():
	Reynolds = [1E3, 10E6] #Reynolds number
	FricFact = [0.01, 0.08] #friction factor

	canvas(x=Reynolds, y=FricFact)
	xscale("log")

	#laminar flow 0<Re<2300
	fD = lambda Re: 64.0/Re
	p1 = (1000, fD(1000))
	p2 = (2300, fD(2300))
	line(p1=p1, p2=p2, lw=2, ls="--")
