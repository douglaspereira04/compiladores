class LL1ParsingResult():
	def __init__(self):
		self._stack = []
		self._input = []
		self._rule = []

		self.tree = None

		self.accepted = False

	def add_entry(self, _stack, _input, _rule):
		self._stack.append(_stack)
		self._input.append(_input)
		self._rule.append(_rule)

	def check(self):
		try:
			self.accepted = (len(self._stack[-1]) == 1) and (self._stack[0][0] == "$")
			self.accepted = self.accepted and (len(self._input[-1]) == 0)
		except IndexError as e:
			self.result = False
