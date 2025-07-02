from typing import Iterable
from .. import scatter, title, xlabel, ylabel, Marker


def scree(eigvals:Iterable[float], axislabel:tuple[str, str]=("Component Number", "Eigenvalue")):
	xvals = [i+1 for i in range(len(eigvals))]

	yvals = [v for v in eigvals]
	yvals.sort(reverse=True)
	
	scatter(x=xvals, y=yvals, marker=Marker(), ls = "-", lw=2)
	title("Scree Plot")
	xlabel(axislabel[0])
	ylabel(axislabel[1])
	