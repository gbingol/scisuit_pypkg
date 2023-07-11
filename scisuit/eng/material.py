from abc import ABC


__all__ = ['Material']


class Material(ABC):
	"""
		Abstract base class for all materials 
	"""
	
	def __init__(self) -> None: 
	      super().__init__()  