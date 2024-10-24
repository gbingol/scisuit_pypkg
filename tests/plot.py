import numpy as np
import scisuit.plot as plt


def bar():
	#stacked bar charts
	categ=["Q1", "Q2", "Q3", "Q4"]
	A = [44, 55, 41, 67]
	B = [13, 23, 8, 13]

	plt.layout(2,1)

	plt.subplot(0,0)
	plt.bar(x=categ, height=A, fc=(0,255,0), label="A", hatch="\\")
	plt.bar(height=B, x=categ, label="B", lw=2, bottom=A)

	plt.subplot(1,0)
	plt.barh(y=categ, width=A, fc=(0,255,0), label="A", hatch="\\")
	plt.barh(width=B, y=categ, label="B", lw=2, bottom=A)


	plt.figure()

	#Clustered bar chart
	Categ = ("Control", "MW", "IR")
	Levels = {
	'A': (18, 18, 14),
	'B': (38, 48, 47),
	'C': (189, 195, 217)}

	x = np.arange(len(Categ))  # the label locations
	width = 0.25  # the width of the bars
	mult = 0

	for key, measure in Levels.items():
		offset = width * mult
		plt.bar(x=x + offset, height=measure, width=width, label=key)
		mult += 1

	plt.set_xticks(x+width, Categ)




def histogram():
	import scisuit.stats as stat

	x=stat.rnorm(100)

	plt.layout(2,2)

	plt.subplot(0,0)
	plt.hist(x, fc="255 0 0", lw=2, ec=[0,255,0])
	plt.title("Freedman Diaconis")

	plt.subplot(1,0)
	plt.hist(x, fc="0 200 50", lw=2, ec=[0,255,255], binmethod="rice")
	plt.title("Rice")

	plt.subplot(0,1)
	plt.hist(x, fc="0 0 255", lw=2, ec=[0,255,0], binmethod="sturges")
	plt.title("Sturges")

	plt.subplot(1, 1)
	plt.hist(x, fc="255 50 100", lw=2, ec=[0,255,0], binmethod="scott")
	plt.title("Scott")

	
	plt.figure()


	plt.layout(2,2)

	plt.subplot(0,0)
	plt.hist(x, fc="255 0 0", lw=2, ec=[0,255,0], density=True)

	plt.subplot(0,1)
	plt.hist(x, fc="255 0 0", lw=2, ec=[0,255,0], density=True, cumulative=True)
	
	plt.subplot(1,0)
	plt.hist(x, breaks=np.linspace(-2,2, 10))
	
	plt.subplot(1,1)
	plt.hist(x, breaks=7)





def qqcharts():
	import scisuit.stats as stat
	x= [24, 43, 58, 71, 43, 49, 61, 44, 67, 49, 53, 56, 59, 52, 62, 54, 57, 33, 46, 43, 57]

	#full control on marker
	plt.layout(1,2)

	plt.subplot(0,0)
	plt.qqnorm(x, lw=5, ec=(0, 255,0), 
			marker=plt.Marker(style="s", fc=(255,0,0), lw=2))


	#marker with default Pen and Brush properties
	plt.subplot(0, 1)
	plt.qqnorm(x, lw=3, marker="s")


	plt.figure()

	t = [24, 33,43,43,43,44,46,49,49,52,53,54,56,57,57,58,59,61,62,67,71]
	c = [10,17,19,20,26,28,33,37,37,41,42,42,42,43,46,48,53,54,55,55,60,62,85]

	plt.qqplot(x=c, y=t, markersize=7, fc="#FF0000")
	plt.title("qqplot")





def quiver():
	#flow visualization example
	x=np.arange(-3.0, 3.0, 0.5)
	y=np.arange(-1.0, 5.0, 0.5)
	X, Y = np.meshgrid(x,y)

	#V= (u, v) = (0.5+0.8x)i + (1.5-0.8y)j
	U= 0.5 + 0.8*X
	V=1.5 - 0.8*Y

	plt.quiver(X,Y,U, V, 
			scale=0.3, 
			lw=3, 
			ec=(0,255, 0), 
			length=0.2, 
			alpha = 0.25)
	plt.title("V= (u, v) = (0.5+0.8x)i + (1.5-0.8y)j")


	plt.figure()

	#visualization of dy/dt=4-t+2y
	tt=np.arange(0.0, 2.0, 0.2)
	yy=np.arange(-5.0, 0.0, 0.2)

	t, y = np.meshgrid(tt,yy) 
	
	f1= 4-t+2*y

	plt.dirfield(t, y, f1) 
	plt.title("dy/dt=4-t+2y")




def boxplot():
	x = [2, 1, 3, 6, 4]
	y = [7, 7, 8, 4, 2]

	plt.boxplot(data=x)
	plt.boxplot(data=y)




def scatter():
	x = np.arange(0, 6, 0.5)
	y = x**2

	plt.layout(2,1)

	#show line and marker with default pen and brush
	plt.subplot(0,0)
	plt.scatter(x=x, y=y, lw=3, ls=":", marker="s", markersize=10)
	print(plt.xlim())

	#customize marker properties
	plt.subplot(1,0)
	plt.scatter(x=x, y=y, marker=plt.Marker(fc="#00FF00"))


	plt.figure()


	L = [80.66, 79.84, 78.6, 72.73, 80.05, 72.49, 68.09, 81.55, 68.6, 78.09]
	F = [1.67, 1.36, 1.84, 2.78, 2, 1.7, 4.77, 2.96, 1.54, 2.05]
	P = [337399, 819023, 55230, 797162, 618015, 731371, 310907, 74856, 1418500, 3070070]

	plt.bubble(x=L, y=F, s=P)




def engcharts():
	plt.moody()
	plt.figure()
	plt.psychrometry()
	plt.legend(3,5)




import scisuit.plot.gdi as gdi
import scisuit.plot as plt
import numpy as np


scatter()

plt.figure()

plt.psychrometry()

#plt.savefig("C:\\Users\\gbing\\Documents\\Visual Studio 2022\\Projects\\scisuit_pypkg\\scisuit\\abc.xpm")



plt.show()