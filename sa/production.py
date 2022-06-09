EPSILON = "&"

class Production():
	def __init__(self, head, products):
		self.head = head
		self.products = products

	def head(self):
		return self.head

	def products(self):
		return self.products

	def is_epsilon(self):
		for p in self.products:
			if(p == EPSILON):
				return True
		return False

	def __str__(self):
		return str(self.__key())

	def __eq__(self, other):
		if(isinstance(other, Production)):
			return self.__key() == other.__key()
		return NotImplemented

	def __ne__(self, obj):
		if(isinstance(other, Production)):
			return self.__key() != other.__key()
		return NotImplemented

	def __key(self):
		return (self.head, tuple(self.products))

	def __hash__(self):
		return hash(self.__key())