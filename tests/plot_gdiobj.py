import sys, os
import numpy as np
import math

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 




def scatter_errorbar():
	import numpy as np
	import math

	#temperatures
	measurement = [0, 20, 50] 

	#Energy absorbed at different temperatures
	data = np.array([
		[52, 58, 82, 35, 84], #0C
		[48, 66, 74, 86, 78], #20
		[73.5, 82, 72, 80, 79] #100C
	])

	mean  = np.mean(data, axis=1)
	std = np.std(data, axis=1, ddof=1)
	se = std/ math.sqrt(data.shape[1])

	plt.canvas(x=[-10,60], y=[40,90])
	for i in range(len(measurement)):
		x1 = measurement[i]
		x2 = x1
		y1, y2 = mean[i] + se[i], mean[i] - se[i]
		gdi.line([x1, y1], [x2, y2], ls = "--", lw=2, ec="#FF0000")

		gdi.marker(xy=(x1,mean[i]))




def drawlines():
	"""Draws similar to letter H"""
	plt.canvas(x=[-5,5], y=[-5,5])

	gdi.line(p1=[-3,-3], p2=[-3, 3], lw=3)
	gdi.line(p1=[3, -3], p2=[3,3], ec="0 10 255", lw=3, ls="--")
	gdi.line(p1=[-3,0], p2=[3,0], lw=3, ls=":", ec="255 0 0")




def drawrects():
	plt.canvas(x=[-5,5], y=[-5,5])

	gdi.rect([-4, -3], width=3, height=4, 
			ec="20 50 100", 
			lw=2, 
			ls="--")
	gdi.rect([0, -1], width=4, height=3, 
			ec="#FF0000", 
			lw=2, 
			fc="0 255 255", 
			hatch="/")
	


def drawrotatedtext():
	"""Text with different rotations"""
	plt.canvas(x=[-5,5], y=[-5,5])

	angles = range(0, 360, 45)
	r = 1
	for alpha in angles:
		rad = alpha*math.pi/180
		loc = [r*math.cos(rad), r*math.sin(rad)]
		gdi.text(loc, label="Hello Python", rotation=alpha)



def drawrotatedarrows():
	"""Arrow with different colors and angles"""
	from random import randrange as rr
	from math import cos, sin, radians

	plt.canvas(x=[-5,5], y=[-5,5])

	r1, r2 = 1.0, 4.0

	p=lambda r, d: [r*cos(radians(d)), r*sin(radians(d))]
	for i in range(0, 360, 45):
		color = [rr(0, 255), rr(0, 255), rr(0, 255)]
		gdi.arrow(p(r1, i), p(r2, i), ec=color, lw=3)




def drawarc():
	"""Draws half circle"""
	plt.canvas(x=[1,7], y=[2,6])

	c, p1, p2 = (4,3), (6, 3), (2,3)

	gdi.arc(center=c , p1=p1, p2=p2, fc="#00FF00")
	gdi.text(xy=c, label="C")
	gdi.text(xy=p1, label="p1")
	gdi.text(xy=p2, label="p2")

	plt.show()



def drawpolygon():
	"""Shows a triangle"""
	plt.canvas(x=[0,6], y=[0,4])

	x = [1,3,5]
	y = [1,3,1]

	#alternatively, list(zip(x,y))
	xy = [(1,1), (3,3), (5,1)]

	gdi.polygon(xy=xy, fc="#FF12AA")




def heart1():
	t= np.linspace(-10, 10, 1000)
	x=np.sin(t)*np.cos(t)*np.log(np.abs(t))
	y=np.abs(t)**0.3*np.sqrt(np.cos(t))



def heart2():
	import numpy as np
	t= np.linspace(-10, 10, 1000)
	x = 16*np.sin(t)**3
	y = 13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)

	plt.canvas(x=[-20, 20], y=[-20, 20], 
		haxis=False, vaxis=False, #axes are not shown
		hgrid=False, vgrid=False) #gridlines are not shown

	gdi.curve(x, y, ec="#FF0000")
	gdi.text((-4.5,-4), "Thank You", 45, 
			fontsize=25, 
			fontcolor="#00FF00")




import scisuit.plot as plt
import scisuit.plot.gdi as gdi
import numpy as np

plt.canvas(x=[0,6], y=[0,4])

x = [1,3,5]
y = [1,3,1]

#alternatively, list(zip(x,y))
xy = [(1,1), (3,3), (5,1)]

gdi.polygon(xy=xy, fc="#FF12AA")

plt.show()

