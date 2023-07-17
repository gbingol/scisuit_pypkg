import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.stats as stat
import scisuit.plot as plt
from scisuit.plot.enums import Marker_Type, Color
import numpy as np



plt.app()




plt.mainloop()






#---------------------------------------------------------------------


"""
#Histogram

import scisuit.stats as stat

x=stat.rnorm(500)

plt.histogram(x)
plt.histogram(x, mode=plt.Histogram_Mode.RELFREQUENCY, cumulative=True)
plt.histogram(x, fill={'color': plt.Color.RED}, line={'color': plt.Color.GREEN, 'width': 2} )
"""




#---------------------------------------------------------------------

"""
#Line Chart

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
"""



#---------------------------------------------------------------------

"""
#Pie Chart

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

"""


#----------------------------------------------------------------------

"""
# Pie of Pie Chart

data=[10, 6, 8, 1, 2]
labels=["A", "B", "C", "D", "E"]
groups=[1, 1, 1, 2, 2]

#Group membership defined
plt.piepie(data, groups=groups)

#TODO: Fix me
plt.piepie(data, groups=groups, lexplode=[2], rexplode = [1] )

#Colors defined (first of left, two of right)
plt.piepie(data, groups=groups, lcolors = ["255 51 153"], rcolors=["153 153 0", "0 153 153"] )

"""


#----------------------------------------------------------------

"""
#QQ Norm 

x=stat.rnorm(100)

#Normal Q-Q chart
plt.qqnorm(x)

#Marker specified
marker = {'fill': Color.WHITE, 'linecolor': Color.BLUE, 'type': Marker_Type.SQUARE, 'linewidth': 2, 'size': 5}
plt.qqnorm(x, marker=marker)
"""


#-----------------------------------------------------------------

"""
treatment = [24, 33,43,43,43,44,46,49,49,52,53,54,56,57,57,58,59,61,62,67,71]
control = [10,17,19,20,26,28,33,37,37,41,42,42,42,43,46,48,53,54,55,55,60,62,85]

plt.qqplot(x=control, y=treatment, xlab="control", ylab="treatment")

marker = {'fill': Color.WHITE, 'linecolor': Color.BLUE, 'type': Marker_Type.SQUARE, 'linewidth': 2, 'size':5}
plt.qqplot(x=control, y=treatment, xlab="control", ylab="treatment", marker = marker)
"""