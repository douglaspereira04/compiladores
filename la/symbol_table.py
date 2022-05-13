from tabulate.tabulate import tabulate

# Holds a symbol table line

class LexemeTableEntry:
    def __init__(self, token_type, lexeme, lineno, lexpos):
    	self.token = token_type
    	self.lexeme = lexeme
    	self.line = lineno
    	self.pos = lexpos

    def __iter__(self):
    	return iter([self.token, self.lexeme, self.line, self.pos])

# Class of a symbol table
class LexemeTable:
    def __init__(self):
    	self.table = []

    def add_token(self, token_type, lexeme, lineno, lexpos):
        self.table.append(LexemeTableEntry(token_type, lexeme, lineno, lexpos))

    def __iter__(self):
    	return iter(self.table)

    def to_string(self):
        return tabulate(tabular_data=self, headers=("TOKEN", "LEXEMA", "LINHA", "POSIÇÃO"), tablefmt="fancy_grid")

    def to_symbol_table_string(self):
        symbol_table_dict = self.symbol_table_dict()
        symbol_table_tuple_list = []

        for lexeme in symbol_table_dict:
            symbol_table_tuple_list.append((lexeme,symbol_table_dict[lexeme]))
        return tabulate(tabular_data=symbol_table_tuple_list, headers=("LEXEMA", "POSIÇÕES"), tablefmt="fancy_grid")

    def last(self):
        return self.table[len(self.table)-1]

    def symbol_table_dict(self):

        idents = list(filter(lambda entry: entry.token == "IDENT", self.table))

        symbol_table = dict()

        for ident in idents:
            if ident.lexeme not in symbol_table:
                symbol_table[ident.lexeme] = []
            symbol_table[ident.lexeme].append((ident.line,ident.pos))

        return symbol_table


