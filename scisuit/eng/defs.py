
class Dielectric:
	def __init__(self, constant, loss) -> None:
		self._Constant =constant
		self._Loss = loss
	
	@property
	def constant(self):
		pass

	@constant.getter
	def constant(self):
		return self._Constant
	
	@property
	def loss(self):
		pass

	@loss.getter
	def loss(self):
		return self._Loss
