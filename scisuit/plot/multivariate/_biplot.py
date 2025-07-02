from typing import Iterable
from .. import scatter, title, xlabel, ylabel, xlim, ylim
from ..gdi import line, text



def biplot(
		scores:Iterable[tuple[float, float]], 
		pc1:Iterable[float], 
		pc2:Iterable[float],
		eigvals:tuple[float, float],
		labels:Iterable[str],
		showcomponent = True,
		axislabel:tuple[str, str]=("First Component", "Second Component")):
	"""
	Plots biplot.  
	The numbers appearing next to markers show observation numbers.  

	scores: An iterable containing scores in the order of first and second components
	pc1: First principal component vector  
	pc2: Second principal component vector  
	eigvals: Eigenvalues corresponding to pc1 and pc2   
	labels: Labels of variables  
	showcomponent: Show each component label?
	"""

	m = map(list, zip(*scores))
	lst = [list(e) for e in m]

	xvals, yvals = lst[0], lst[1]

	scatter(x=xvals, y=yvals)
	title("Biplot")
	xlabel(axislabel[0])
	ylabel(axislabel[1])

	if showcomponent:
		#Let's show observation numbers
		for i in range(len(xvals)):
			x, y =xvals[i], yvals[i]
			text(xy=(x, y), label=f" {i+1}", vanchor="c") #space in numbering is intentional
	

	pc1_scaled = [v*eigvals[0] for v in pc1]
	pc2_scaled = [v*eigvals[1] for v in pc2]
	for i in range(len(labels)):
		label = labels[i]
		xend, yend =pc1_scaled[i], pc2_scaled[i]
		xbegin, ybegin = 0, 0

		line(p1=(xbegin, ybegin), p2=(xend, yend))
		text(xy=(xend, yend), label=label, hanchor="c", vanchor="b")