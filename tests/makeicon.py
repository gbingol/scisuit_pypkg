import sys, os

#inserting to 0th position is very important so that search will FIRST match ../scisuit folder
sys.path.insert(0, os.getcwd()) 


import wx
from scisuit.wxpy import makeicon
from scisuit.util import parent_path

path = parent_path(__file__)

app = wx.App()

frm = wx.Frame(None)
frm.SetIcon(makeicon(path/"fluid.bmp"))
frm.Show()
app.MainLoop()