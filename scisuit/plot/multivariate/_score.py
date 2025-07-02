from typing import Iterable
from .. import scatter, title, xlabel, ylabel, xlim, ylim
from ..gdi import line, text

def score(scores:Iterable[tuple[float, float]], axislabel:tuple[str, str]=("First Component", "Second Component")):
	"""
	Plots score plot.  
	The numbers appearing next to markers show observation numbers.  

	scores: An iterable containing scores in the order of first and second components
	"""

	m = map(list, zip(*scores))
	lst = [list(e) for e in m]

	xvals, yvals = lst[0], lst[1]

	scatter(x=xvals, y=yvals)
	title("Score Plot")
	xlabel(axislabel[0])
	ylabel(axislabel[1])

	xbegin, xend = xlim()
	y0, y1 = ylim()
	line(p1=(xbegin, 0), p2=(xend, 0), ls="--", ec="#FF0000A3")
	line(p1=(0, y0), p2=(0, y1), ls="--", ec="#FF0000")

	#Let's show observation numbers
	for i in range(len(xvals)):
		x, y =xvals[i], yvals[i]
		text(xy=(x, y), label=f" {i+1}", vanchor="c") #space in numbering is intentional