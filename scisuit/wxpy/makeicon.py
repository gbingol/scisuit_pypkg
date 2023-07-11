import os as _os
import wx as _wx
from pathlib import Path as _Path

def makeicon(path:_Path)->_wx.Icon:
	"""
	path: image's full path 
	"""

	if(not path.is_absolute()):
		raise ValueError(path + " is relative path, full path expected.")
		
	if(not path.exists()):
		raise ValueError("Invalid path: " + path)

	icon = _wx.Icon()
	image = _wx.Image()
	image.LoadFile(str(path))
	bmp=image.ConvertToBitmap()
	icon.CopyFromBitmap(bmp)

	return icon


