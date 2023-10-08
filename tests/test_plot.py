import sys, os
import numpy as np

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.stats as stat
import scisuit.plot as plt



def bar():
	categ=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	plt.bar(labels=categ, height=A, style=plt.PERCENTSTK)
	plt.bar(height=B, style=plt.PERCENTSTK)
	plt.show()


def histogram():
	import scisuit.stats as stat

	x=stat.rnorm(500)
	plt.histogram(x,  
			fill=plt.Brush(color=plt.Color.RED), 
			line=plt.Pen(color="0 255 0", width=2))
	plt.show()



def linechart():
	categories=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	#Line (Unstacked)
	plt.line(labels=categories, y=A)

	#Clustered line chart with two series
	hwnd = plt.line(labels=categories, y=A)
	plt.line(y=B, hwnd=hwnd)

	#Stacked line chart with two series
	hwnd = plt.line(labels=categories, y=A, type=plt.Line_Type.STACKED)
	plt.line(y=B, type=plt.Line_Type.STACKED, hwnd=hwnd)

	#%-stacked with two series
	hwnd = plt.line(labels=categories, y=A, type=plt.Line_Type.PERCENTSTK)
	plt.line(y=B, type=plt.Line_Type.PERCENTSTK, hwnd=hwnd)



def pie():
	data=[10, 6, 8]

	#labels have been automatically assigned as 1, 2 and 3.
	plt.pie(data)

	#Labels explicitly defined
	plt.pie(data, labels=["A", "B", "C"])

	#Number of labels less than slices
	plt.pie(data, labels=["A"])

	#Explosion of whole pie
	plt.pie(data, explode = 1)

	#Explosion of only first slice
	plt.pie(data, explode = [1] )

	#arbitrary colors for each slice.
	plt.pie(data, colors = [plt.Color.GREEN, plt.Color.RED, plt.Color.CHOCOLATE] )

	#set the angle of first slice to 45°.
	plt.pie(data, startangle=45)



def qqnorm():
	x=stat.rnorm(100)

	#Normal Q-Q chart
	plt.qqnorm(x)

	#Marker specified
	marker = {'fill': plt.Color.WHITE, 'linecolor': plt.Color.BLUE, 'type': plt.MARKER_SQUARE, 'linewidth': 2, 'size': 5}
	plt.qqnorm(x, marker=marker)



def qqplot():
	treatment = [24, 33,43,43,43,44,46,49,49,52,53,54,56,57,57,58,59,61,62,67,71]
	control = [10,17,19,20,26,28,33,37,37,41,42,42,42,43,46,48,53,54,55,55,60,62,85]

	plt.qqplot(x=control, y=treatment)

	marker = {'fill': plt.Color.WHITE, 'linecolor': plt.Color.BLUE, 'type': plt.MARKER_SQUARE, 'linewidth': 2, 'size':5}
	plt.qqplot(x=control, y=treatment, marker = marker)




def quiver():
	x=np.arange(-3.0, 3.0, 0.5)
	y=np.arange(-1.0, 5.0, 0.5)
	X, Y = np.meshgrid(x,y)

	#V= (u, v) = (0.5+0.8x)i + (1.5-0.8y)j
	U= 0.5 + 0.8*X
	V=1.5 - 0.8*Y

	#without scaling
	plt.quiver(X,Y, U, V)

	#with scaling
	plt.quiver(X,Y, U, V, scale = True)



def dirfield():
	t=np.arange(0.0, 2.0, 0.2)
	y=np.arange(-5.0, 0.0, 0.2)

	t, y = np.meshgrid(t,y) 
	
	f1= 4-t+2*y

	plt.dirfield(t,y,f1) 


def matplotlib_mixed():
	import matplotlib.pyplot as plt
	fruits = ['apple', 'blueberry', 'cherry', 'orange']
	counts = [40, 100, 30, 55]
	bar_labels = ['red', 'blue', '_red', 'orange']
	bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

	plt.bar(fruits, counts, label=bar_labels, color=bar_colors)
	plt.plot([1,2,3], [1, 4, 9])
	plt.show()

def boxplot():
	x = [2, 1, 3, 6, 4]
	y = [7, 7, 8, 4, 2]

	plt.boxplot(data=x)
	plt.boxplot(data=y)



import scisuit.plot as plt

treatment = [24, 33,43,43,43,44,46,49,49,52,53,54,56,57,57,58,59,61,62,67,71]
control = [10,17,19,20,26,28,33,37,37,41,42,42,42,43,46,48,53,54,55,55,60,62,85]

plt.qqplot(x=control, y=treatment, 
	     marker=plt.Marker(
		     style=plt.Marker.STYLE.SQUARE,
		     size=5,
		     fill=plt.Brush(color="255 255 255"),
		     line=plt.Pen(color="0 0 255", width=2))
)
plt.show()