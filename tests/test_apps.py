import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
#sys.path.insert(0, os.getcwd()) 

import wx
import ctypes

from scisuit.apps import frmPsychrometry, frmFluidProperties

#Important otherwise colors/text of app looks blurry
ctypes.windll.shcore.SetProcessDpiAwareness(True)

app = wx.App()

frm1 = frmPsychrometry()
frm1.Show()

frm2 = frmFluidProperties()
frm2.Show()

app.MainLoop()
