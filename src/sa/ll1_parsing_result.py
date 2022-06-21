class LL1ParsingResult():
	def __init__(self):
		self._stack = []
		self._input = []
		self._rule = []

		self.tree = None

		self.accepted = False
		self.fs = None
		self.unmatched_token = None

	def add_entry(self, _stack, _input, _rule):
		self._stack.append(_stack)
		self._input.append(_input)
		self._rule.append(_rule)

	def check(self):
		try:
			self.accepted = (len(self._stack[-1]) == 1) and (self._stack[0][0] == "$")
			self.accepted = self.accepted and (len(self._input[-1]) == 0)
		except IndexError as e:
			self.accepted = False

		if(self.accepted == False):
			try:
				self.load_error()
			except Exception as e:
				self.fs = None
		else:
			self.fs = None


	def load_error(self):
		self.fs = (self._input[0][:-(len(self._input[-1]))])+list(reversed(self._stack[-1][1:]))
		self.unmatched_token = self._input[-1][0]
