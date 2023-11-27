import os as _os
import sys as _sys
from pathlib import Path as _Path



def parent_path(path:str, level = 0)->_Path:
	"""
	This is used so many times that a convenience function is deemed appropriate.

	## Input: 
	path: Relative or full path 
	
	## Example:
	if path is C:\\a\\b\\c.py  \n
	level=0 => C:\\a\\b \n
	level=1 => C:\\a
	
	"""
	pt = _Path(path)

	if(pt.is_absolute() == False):
		pt = pt.absolute()

	return pt.parents[level]



def pyhomepath()->str:
	"""
	returns the Python Home Path
	"""
	return _sys.exec_prefix
