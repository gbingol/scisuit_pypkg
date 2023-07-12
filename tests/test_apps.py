import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 

import wx

from scisuit.apps import frmPsychrometry

app = wx.App(useBestVisual=True)

frm = frmPsychrometry(None, False)
frm.Show()

app.MainLoop()
