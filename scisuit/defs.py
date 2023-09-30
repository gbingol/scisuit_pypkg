def override(aclass):
	def overrider(method):
		assert(method.__name__ in dir(aclass))
		return method
	return overrider