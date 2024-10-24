from ctypes import PyDLL
from sys import version_info
from pathlib import Path as _Path


#Tested with: 3.10.6, 3.11.6, 3.12.0, 3.13
_DLLname = f"pybind{version_info.major}{version_info.minor}"

#__file__ is guaranteed to be an absolute path in Python 3.9+
__pt = _Path(__file__)
pydll = PyDLL(str(__pt.parents[0] / _DLLname))


__all__ = ['pydll']