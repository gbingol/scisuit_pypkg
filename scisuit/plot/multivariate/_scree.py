from typing import Iterable
from .. import scatter, title, xlabel, ylabel, Marker


def scree(eigvals:Iterable[float], labels:tuple[str, str]=("Component Number", "Eigenvalue")):
	xvals = [i+1 for i in range(len(eigvals))]
	scatter(x=xvals, y=eigvals, marker=Marker(), ls = "-", lw=2)
	title("Scree Plot")
	xlabel(labels[0])
	ylabel(labels[1])
	