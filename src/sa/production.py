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

		if(len(self.products) == 1):
			if(self.products[0] == EPSILON):
				return True
		return False

	def is_direct_left_recursive(self):
		return self.products[0] == self.head

	def __str__(self):
		return str(self.__key())

	def __eq__(self, other):
		if(other != None):
			if(isinstance(other, Production)):
				return self.__key() == other.__key()
		return False

	def __ne__(self, other):
		return not(self == other)

	def __key(self):
		return (self.head, tuple(self.products))

	def __hash__(self):
		return hash(self.__key())

	def __str__(self):
		string = self.head + " ->"
		for product in self.products:
			string += " "+product
		return string