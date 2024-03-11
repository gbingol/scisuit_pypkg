import math



class NiceNumbers:
	def __init__(self, minimum, maximum, maxticks=10) -> None:
		self._min = minimum
		self._max = maximum
		self._maxticks = maxticks

		self._calculate()
	

	def _calculate(self):
		_range = self._nicenum(self._max - self._min, False)
		self._tickspacing = self._nicenum(_range / (self._maxticks - 1), True)

		self._nicemin = math.floor(self._min / self._tickspacing) * self._tickspacing
		self._nicemax = math.ceil(self._max / self._tickspacing) * self._tickspacing


	def _nicenum(self, Range:float, Round:bool):
		exponent = math.floor(math.log10(Range))
		frac = Range / math.pow(10, exponent)

		if Round:
			if frac < 1.5: niceFrac = 1
			elif frac < 3: niceFrac = 2
			elif frac < 7: niceFrac = 5
			else: niceFrac = 10
		else:
			if frac <= 1: niceFrac = 1
			elif frac <= 2: niceFrac = 2
			elif frac <= 5: niceFrac = 5
			else: niceFrac = 10

		return niceFrac * math.pow(10.0, exponent)

	@property
	def nicemin(self):
		return self._nicemin

	@property
	def nicemax(self):
		return self._nicemax
	
	@property
	def tickspace(self):
		return self._tickspacing
	

"""
if __name__ == "__main__":
	n = NiceNumbers(0.5, 10.25)
	print(n.nicemax, " ", n.nicemin, " ", n.tickspace)
	
"""
