import sys, os
import numpy as np
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 




def scatter_errorbar():

	import math
	import numpy as np
	import scisuit.plot as plt


	measurement = [0, 20, 100] #temperatures

	#Energy absorbed at different temperatures
	data = np.array([
		[52, 58, 82, 35, 84], #0C
		[48, 66, 74, 86, 78], #20
		[73.5, 82, 72, 80, 79] #100C
	])

	mean  = np.mean(data, axis=1)
	std = np.std(data, axis=1, ddof=1)
	se = std/ math.sqrt(data.shape[1])

	plt.scatter(x = measurement, y = mean)
	for i in range(len(measurement)):
		x1 = measurement[i]
		x2 = x1
		y1, y2 = mean[i] + se[i], mean[i] - se[i]
		gdi.line([x1, y1], [x2, y2], edgecolor = plt.C_BLACK, ls = "--", lw=2)




import scisuit.plot as plt
import scisuit.plot.gdi as gdi




#gdi.arc(center = (4,3), p1=(6, 3), p2=(2,3),  
#		pen=gdi.Pen(plt.COLOR_GREEN, width=3), 
#		brush=gdi.Brush(plt.COLOR_BROWN, plt.BRUSH_FDIAGHATCH))

def heart1():
	t= np.linspace(-10, 10, 1000)
	#x=np.sin(t)*np.cos(t)*np.log(np.abs(t))
	#y=np.abs(t)**0.3*np.sqrt(np.cos(t))



def heart2():
	t= np.linspace(-10, 10, 1000)
	x = 16*np.sin(t)**3
	y = 13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)

	plt.canvas(xmin=-20, xmax=20, ymin=-20, ymax=20)

	gdi.curve(x, y, pen = gdi.Pen(plt.C_RED))
	gdi.text((-4.5,-4), "text", 45, 
			font= gdi.Font(size=25, color=plt.C_GREEN))





import scisuit.plot as plt
import scisuit.plot.gdi as gdi
import numpy as np



x = [32, 42, 110, 115, 118, 145, 150]
y = [1400, 1800, 1750, 1900, 2600, 2210, 2450]



#plot a simple scatter chart
plt.scatter(x=x, y=y, lw=1, ec="0 255 0", markersize=10, )

poly = np.polyfit(x, y, 1)

for i in range(len(x)):
	rv = np.polyval(poly, x[i])
	#experimental data
	p1 = (x[i], y[i])

	#regression data
	p2 = (x[i], rv)

	label = str(int(y[i] -rv))

	gdi.line(p1, p2, ls="-", lw=4, label=label )

gdi.rect([50, 2000], width=50, height=500, hatch="\\", facecolor=(255, 0, 0))

plt.show()


