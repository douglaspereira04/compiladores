# Douglas Pereira Luiz

from texttable.texttable import Texttable

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
        table = Texttable()
        rows = []
        
        rows.append(["TOKEN", "LEXEMA", "LINHA", "POSIÇÃO"])
        for entry in self.table:
                rows.append([entry.token, entry.lexeme, str(entry.line), str(entry.pos)])

        table.add_rows(rows)

        return table.draw()

    def to_symbol_table_string(self):
        symbol_table_dict = self.symbol_table_dict()
        symbol_table_tuple_list = []

        headers = None

        table = Texttable()
        rows = []
        if(len(self.ident) > 1):
            rows.append(["TOKEN", "LEXEMA", "POSIÇÕES"])

            for (token,lexeme) in symbol_table_dict:
                amount = 0
                posentry = ""
                for pos in symbol_table_dict[(token,lexeme)]:
                    posentry = posentry + str(pos) + ", "

                    if(amount == 20):
                        posentry = posentry +"\n"
                        amount = 0
                    else:
                        amount = amount + 1

                rows.append([token, lexeme, posentry])

        else:
            rows.append(["LEXEMA", "POSIÇÕES"])
            for (token,lexeme) in symbol_table_dict:
                amount = 0
                posentry = ""
                for pos in symbol_table_dict[(token,lexeme)]:
                    posentry = posentry + str(pos) + ", "

                    if(amount == 20):
                        posentry = posentry +"\n"
                        amount = 0
                    else:
                        amount = amount + 1

                rows.append([lexeme, posentry])

        table.add_rows(rows)

        return table.draw()

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


