import wx
import os
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
	## Input: 
	Name: package name, (wx) \n
	pip: pip install name (wxPython) 

	## Return: 
	if package is already installed returns True \n

	If missing, prompts the user (wx.MessageBox) to install the package, \n
	if user clicks No, returns False, \n
	if user clicks Yes, installation process begins and function returns True
	"""

	#package already installed
	if(pkg_installed(name)):
		return True
	
	PyHome = pyhomepath()
	PyExe = PyHome + os.sep + "python.exe"
	Cmd = "\"" + PyExe + "\""
	Cmd += " -m pip install " + pip

	Msg = name + " is missing. Wanna install? \n \n"
	Msg += "Choosing Yes will launch the terminal and installation process using the following command: \n \n"
	
	Msg += Cmd + "\n \n"

	Msg += "If you choose No, you might have to manually install the package to run the requiring app."

	YesNo = wx.MessageBox(Msg, "Install " + name + "?", wx.YES_NO)
	if (YesNo == wx.NO):
		return False

	wx.Shell(Cmd)

	return True
