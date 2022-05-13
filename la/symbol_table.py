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
    def __init__(self, ident):
        self.table = []
        self.ident = ident

    def add_token(self, token_type, lexeme, lineno, lexpos):
        self.table.append(LexemeTableEntry(token_type, lexeme, lineno, lexpos))

    def __iter__(self):
    	return iter(self.table)

    def to_string(self):
        return tabulate(tabular_data=self, headers=("TOKEN", "LEXEMA", "LINHA", "POSIÇÃO"), tablefmt="fancy_grid")

    def to_symbol_table_string(self):
        symbol_table_dict = self.symbol_table_dict()
        symbol_table_tuple_list = []

        headers = None
        if(len(self.ident) > 1):
            for (token,lexeme) in symbol_table_dict:
                symbol_table_tuple_list.append((token,lexeme,symbol_table_dict[(token,lexeme)]))
                headers=("TOKEN","LEXEMA", "POSIÇÕES")
        else:
            for (token,lexeme) in symbol_table_dict:
                symbol_table_tuple_list.append((lexeme,symbol_table_dict[(token,lexeme)]))
                headers=("LEXEMA", "POSIÇÕES")

        return tabulate(tabular_data=symbol_table_tuple_list, headers=headers, tablefmt="fancy_grid")

    def last(self):
        return self.table[len(self.table)-1]

    def symbol_table_dict(self):

        idents = list(filter(lambda entry: entry.token in self.ident, self.table))

        symbol_table = dict()

        for ident in idents:
            if (ident.token,ident.lexeme) not in symbol_table:
                symbol_table[(ident.token,ident.lexeme)] = []
            symbol_table[(ident.token,ident.lexeme)].append((ident.line,ident.pos))

        return symbol_table


