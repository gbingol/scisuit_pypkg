
""" import scisuit.plot.gdi as gdi
import scisuit.plot as plt
import numpy as np

x = np.arange(0, 6, 0.5)

plt.scatter(x=x, y=x**2, lw=3, ls=":", marker="s")
plt.scatter(x=x, y=x, lw=3, ls=":", marker="s")
plt.scatter(x=x, y=2*x, lw=3, ls=":", marker="x", label = "2x")
id1 = gdi.line(p1=(1,1), p2=(3,5), label="line")
id2 = gdi.rect(xy=(1,1), height=5, width=4, label="rect", fc="#FF0000", hatch="/")

gdi.makegroup(id1, [id2])

plt.legend(3,2)
plt.show() """