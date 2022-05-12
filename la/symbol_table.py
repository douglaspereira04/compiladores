from tabulate.tabulate import tabulate

# Holds a symbol table line
class SymbolTableEntry:
    def __init__(self, token):
    	self.token = token.type
    	self.value = token.value
    	self.line = token.lineno
    	self.pos = token.lexpos

    def __iter__(self):
    	return iter([self.token, self.value, self.line, self.pos])

# Class of a symbol table
class SymbolTable:
    def __init__(self):
    	self.table = []

    def add_token(self, token):
        self.table.append(SymbolTableEntry(token))

    def __iter__(self):
    	return iter(self.table)

    def to_string(self):
    	return tabulate(tabular_data=self, headers=("TOKEN", "LEXEMA", "LINHA", "POSIÇÃO"), tablefmt="fancy_grid")