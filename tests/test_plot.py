import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

import wx
import ctypes

import scisuit.plot as plt



pltapp = plt.app()


#psychrometry(P=100000, Tdb=[0,80])

x = [1, 2, 3, 4]
y = [1, 3, 7, 14]

plt.scatter(x=x, y=y)

plt.mainloop()

print("after main")