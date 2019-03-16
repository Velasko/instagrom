class BasicItem():

	def __new__(cls, *args, **kwargs):
		obj = object.__new__(cls)

		obj.__init__(*args, **kwargs)

		#Checks for the necessery methods are implemented
		obj.get_keys()
		obj.__eq__(obj)
		#End of check block

		return obj

	def __post_init__(self):
		self.auto_key()

	def auto_key(self):
		return

	def __eq__(self, other):
		if not isinstance(other, type(self)): return False

		for attr in self.get_keys():
			if getattr(self, attr) != getattr(other, attr):
				return False

		return True

	def serialize(self, *args, **kwargs):
		""""Method responsible for the database interpret the object.
		default is self.__dict__"""

		return self.__dict__