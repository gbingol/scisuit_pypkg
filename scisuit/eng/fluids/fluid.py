from ..material_empirical import EmpiricalMaterial

__all__ = ['Fluid']


class Fluid(EmpiricalMaterial):
	"""
		Abstract base class for all fluids <br>
		Currently, a fluid is assumed to be an empirical material
	"""
	
	def __init__(self) -> None: 
		super().__init__()
