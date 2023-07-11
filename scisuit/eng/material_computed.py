from .material import Material


__all__ = ['ComputedMaterial']


class ComputedMaterial(Material):
	"""
	Base class for all materials whose properties are computed
	"""
	def __init__(self) -> None: 
	      super().__init__()  