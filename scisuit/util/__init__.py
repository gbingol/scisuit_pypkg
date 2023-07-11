import math as _math


def colnum2labels(num:int):
	"""
	Finds the corresponding letter to num.
	For example A=1, B=2, Z=26, AA=27, AB=28, ACR=772, BCK=1441
	"""

	assert num>0, "num must be greater than 0"
	if(type(num) != int):
		raise TypeError("num type must be int")

	Str =""

	NChars = int(_math.ceil(_math.log(num) / _math.log(26.0)))
	if NChars == 1:
		modular = num % 26
		if (modular == 0):
			modular = 26
		Str = chr(65 + modular - 1)
		return Str
	
	val = num
	tbl = []
	for i in range(NChars-1):
		val /= 26
		tbl.append(chr(65 + int(val % 26) - 1))
	
	tbl.reverse()
	Str = "".join(tbl)
	Str += chr(65 + int(num % 26) - 1)

	return Str



from .path import parent_path
from .pkg import pkg_installed, assert_pkg
