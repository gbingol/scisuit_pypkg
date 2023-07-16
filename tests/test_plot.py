import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

import wx

import scisuit.plot as plt

import numpy as np
import scisuit.stats as stat



plt.app()



plt.mainloop()


"""
#Test Histogram

x=stat.rnorm(500)

plt.histogram(x)
plt.histogram(x, mode=plt.Histogram_Mode.RELFREQUENCY, cumulative=True)
plt.histogram(x, fill={'color': plt.Color.RED}, line={'color': plt.Color.GREEN, 'width': 2} )

"""