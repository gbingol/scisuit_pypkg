from typing import Iterable
from .. import canvas, title, xlabel, ylabel
from ..gdi import line, text

def loading(
		pc1:Iterable[float], 
		pc2:Iterable[float], 
		labels:Iterable[str], 
		axislabel:tuple[str, str]=("First Component", "Second Component")):
	"""
	Plots loading plot.  

	pc1: First principal component vector  
	pc2: Second principal component vector  
	labels: Labels of variables
	"""

	assert len(pc1) == len(pc2), "Length of principal components (pc1, pc2) must be equal."
	assert len(labels) == len(pc1), "Principal components and labels must have same lengths."

	xmin, xmax = pc1[0], pc1[0]
	ymin, ymax = pc2[0], pc2[0]

	for i in range(len(pc1)):
		xmin = min(xmin, pc1[i])
		xmax = max(xmax, pc1[i])

		ymin = min(ymin, pc2[i])
		ymax = max(ymax, pc2[i])
		
	expansion = 0.2 #expand axis by 

	xmin = xmin*(1 + expansion)
	xmax = xmax*(1 + expansion)
	ymin = ymin*(1 + expansion)
	ymax = ymax*(1 + expansion)

	canvas(x=(round(xmin, 2), round(xmax, 2)), y=(round(ymin, 2), round(ymax,2)))
	title("Loading Plot")
	xlabel(axislabel[0])
	ylabel(axislabel[1])
	
	for i in range(len(labels)):
		label = labels[i]
		xend, yend =pc1[i], pc2[i]
		xbegin, ybegin = 0, 0

		line(p1=(xbegin, ybegin), p2=(xend, yend))
		text(xy=(xend, yend), label=label, hanchor="c", vanchor="b")