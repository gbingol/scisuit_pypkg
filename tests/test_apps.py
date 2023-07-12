import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

import wx
import ctypes

from scisuit.apps import frmPsychrometry

#Important otherwise colors/text of app looks blurry
ctypes.windll.shcore.SetProcessDpiAwareness(True)

app = wx.App()

frm = frmPsychrometry()
frm.Show()

app.MainLoop()
