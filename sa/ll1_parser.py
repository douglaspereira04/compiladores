
EPSILON = "&"

class g_set(set):
	def __init__(self):
		super().__init__()

	def add(self,item):
		added = not (item in self)
		super().add(item)
		return added


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


class LL1Parser():
	def __init__(self, grammar):
		self.grammar = grammar
		self.alphabet = None
		self.terminals = None
		self.non_terminals = None
		self.productions = None
		self.first_pos = None
		self.parsing_table = None
		self.load_grammar()
		self.load_first_pos()
		self.load_follow_pos()
		self.load_parsing_table()



	def load_grammar(self):
		self.alphabet = set()
		self.non_terminals = set()
		self.productions = []

		lines = self.grammar.split("\n")

		for line in lines:
			productions = line.split("->")
			if(len(productions) != 2):
				continue

			head = productions[0].strip()
			tail = productions[1].split()

			self.alphabet.add(head)
			self.non_terminals.add(head)

			self.productions.append(Production(head, tail))
			for symbol in tail:
				if(symbol != EPSILON):
					self.alphabet.add(symbol)


		self.terminals = self.alphabet - self.non_terminals

		self.first_pos = dict()
		self.follow_pos = dict()
		self.parsing_table = dict()

		for non_terminal in self.non_terminals:
			self.follow_pos[non_terminal] = g_set()
			self.first_pos[non_terminal] = g_set()
			self.parsing_table[non_terminal] = dict()
			for terminal in self.terminals:
				self.parsing_table[non_terminal][terminal] = g_set()

	def load_first_pos(self):

		collected = True

		while(collected):
			collected = False

			for production in self.productions:

				if (production.is_epsilon()):
					collected =  collected or self.first_pos[production.head].add(EPSILON)
				else:
					collected = collected or self.collect_firsts(production)

	"""
	return false if no first was collected
	return true otherwise
	"""
	def collect_firsts(self, production):
		products = production.products
		firsts = self.first_pos[production.head]

		added = False

		epsilon_in_firsts = True

		for symbol in products:
			epsilon_in_firsts = False

			if(symbol in self.terminals):
				added = added or firsts.add(symbol)
				break

			for first in self.first_pos[symbol]:
				epsilon_in_firsts = epsilon_in_firsts or (first == EPSILON)
				added = added or firsts.add(first)
				
			if(not epsilon_in_firsts):
				break

		if(epsilon_in_firsts):
			added = added or firsts.add(EPSILON)

		return added

	def load_follow_pos(self):

		collected = True

		while(collected):
			collected = False

			first_production = True
			for production in self.productions:
				head = production.head
				if(first_production):
					collected = self.follow_pos[head].add("$")
					first_production = False

				for i in range(0,len(production.products)):
					symbol = production.products[i]

					if symbol in self.non_terminals:
						after_symbols = production.products[i+1:]
						after_firsts = self.collect_terminals_and_firsts(after_symbols)

						for first in after_firsts:
							if(first == EPSILON):
								for follow in self.follow_pos[head]:
									collected = collected or self.follow_pos[symbol].add(follow)
							else:
								collected = collected or self.follow_pos[symbol].add(first)


						
						
	def collect_terminals_and_firsts(self, symbols):
		firsts = []
		has_epsilon = True
		for symbol in symbols:
			has_epsilon = False

			if(symbol in self.terminals):
				firsts.append(symbol)
				break
			
			for first in self.first_pos[symbol]:
				has_epsilon = has_epsilon or firsts == EPSILON
				firsts.append(first)

			has_epsilon = has_epsilon or (len(self.first_pos[symbol]) == 0)
			if(not has_epsilon):
				break

		if(has_epsilon):
			firsts.append(EPSILON)

		return firsts


	def load_parsing_table(self):

		for production in self.productions:
			products = production.products.copy()
			if(EPSILON in products):
				products.remove(EPSILON)

			products_firsts = self.collect_terminals_and_firsts(products)
			for symbol in products_firsts:
				if(symbol != EPSILON):
					self.parsing_table[production.head][symbol].add(str(production))
				else:
					follows = self.follow_pos[production.head]
					for follow in follows:
						self.parsing_table[production.head][follow].add(str(production))




