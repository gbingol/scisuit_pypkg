from typing import Iterable
from .. import scatter, title, xlabel, ylabel, xlim, ylim
from ..gdi import line, text


def outlier(distances:Iterable[float], reference:float|None = None, axislabel:tuple[str, str]=("Observation", "Mahalanobis Distance")):
	xvals = [i+1 for i in range(len(distances))]
	scatter(x=xvals, y=distances)
	title("Outlier Plot")
	xlabel(axislabel[0])
	ylabel(axislabel[1])

	if reference != None:
		assert isinstance(reference, float), "if provided reference must be a float" 
		xbegin, xend = xlim()
		ybegin, yend = ylim()

		if reference>yend:
			ylim(ybegin, reference)
		
		line(p1=(xbegin, reference), p2=(xend, reference), ls="--", lw=2, ec="#00FF6A58")
		
		xmid = (xbegin + xend)/2
		text(xy = (xmid, reference), label="Reference line", vanchor="b")

	