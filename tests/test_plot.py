import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import scisuit.plot as plt
import numpy as np



plt.app()




plt.mainloop()






"""
#Histogram

import scisuit.stats as stat

x=stat.rnorm(500)

plt.histogram(x)
plt.histogram(x, mode=plt.Histogram_Mode.RELFREQUENCY, cumulative=True)
plt.histogram(x, fill={'color': plt.Color.RED}, line={'color': plt.Color.GREEN, 'width': 2} )
"""


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