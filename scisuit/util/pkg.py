import wx
import pkgutil
from .path import pyhomepath


__all__=['pkg_installed', 'assert_pkg']


def pkg_installed(name:str)->bool:
	"""
	checks if the package with given name installed \n

	For example, wxPython's package name is wx but pip installation
	requires wxPython. Here the name parameter is wx.
	"""
	
	x = pkgutil.iter_modules()
	for i in x:
		if i.ispkg==True and i.name == name:
			return True
	
	return False


def assert_pkg(name:str, pip:str)->bool:
	"""
	Name: package name, (wx) \n
	pip: pip install name (wxPython) \n

	if package is not missing returns True \n

	If missing, prompts the user to install the package,
	if user rejects, returns False, otherwise returns True
	"""

	#package already installed
	if(pkg_installed(name)):
		return True

	Msg = name + " is missing. Wanna install?"

	YesNo = wx.MessageBox(Msg, "Install " + name + "?", wx.YES_NO)
	if (YesNo == wx.NO):
		return False

	PyHome = pyhomepath()
	PyExe = PyHome + "/python.exe"
	Cmd = "\"" + PyExe + "\""
	Cmd += " -m pip install " + pip

	wx.Shell(Cmd)

	return True
