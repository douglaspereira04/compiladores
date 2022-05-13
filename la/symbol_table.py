from tabulate.tabulate import tabulate

# Holds a symbol table line
class SymbolTableEntry:
    def __init__(self, token_type, value, lineno, lexpos):
    	self.token = token_type
    	self.value = value
    	self.line = lineno
    	self.pos = lexpos

    def __iter__(self):
    	return iter([self.token, self.value, self.line, self.pos])

# Class of a symbol table
class SymbolTable:
    def __init__(self):
    	self.table = []

    def add_token(self, token_type, value, lineno, lexpos):
        self.table.append(SymbolTableEntry(token_type, value, lineno, lexpos))

    def __iter__(self):
    	return iter(self.table)

    def to_string(self):
    	return tabulate(tabular_data=self, headers=("TOKEN", "LEXEMA", "LINHA", "POSIÇÃO"), tablefmt="fancy_grid")

    def last(self):
        return self.table[len(self.table)-1]