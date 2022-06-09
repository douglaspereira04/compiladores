from sa.node import Node
from sa.production import Production, EPSILON
from sa.ll1_parsing_result import LL1ParsingResult


"""
set tha when you add it returns true 
if there was not that item in the set
"""
class g_set(set):
	def __init__(self):
		super().__init__()

	def add(self,item):
		added = not (item in self)
		super().add(item)
		return added


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
		self.non_terminals = []
		self.productions = []

		lines = self.grammar.split("\n")

		for line in lines:
			productions = line.split("->")
			if(len(productions) != 2):
				continue

			head = productions[0].strip()
			tail = productions[1].split()

			self.alphabet.add(head)
			self.non_terminals.append(head)

			self.productions.append(Production(head, tail))
			for symbol in tail:
				if(symbol != EPSILON):
					self.alphabet.add(symbol)


		self.terminals = self.alphabet - set(self.non_terminals)

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
					self.parsing_table[production.head][symbol].add(production)
				else:
					follows = self.follow_pos[production.head]
					for follow in follows:
						self.parsing_table[production.head][follow].add(production)




	def parse(self, symbol_list, max_steps):
		result = LL1ParsingResult()

		tree = Node("ROOT")


		stack = ["$", self.non_terminals[0]]
		parents = [tree]

		i = 0
		index = 0
		while((i < max_steps) and (1 < len(stack))):
			top = stack[-1]

			symbol = None
			try:
				symbol = symbol_list[index] 
			except Exception as e:
				symbol = "$"

			rule = None

			if(top == symbol):

				del stack[-1]
				index +=1
				Node(symbol, parents[-1])
				del parents[-1]

			elif(top in self.non_terminals):

				top_node = Node(top, parents[-1])
				del parents[-1]

				rule = self.parsing_table[top][symbol]
				if not rule:
					break

				del stack[-1]
				products = list(reversed(list(rule)[0].products))

				for product in products:
					parents.append(top_node)

				if(not(EPSILON in products)):
					stack += products
				else:
					Node(EPSILON, parents[-1])
					del parents[-1]

			else:
				break

			result.add_entry(stack, symbol_list[index:], rule)

			i+=1
		result.tree = tree
		result.check()

		return result