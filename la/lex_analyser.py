

# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
import codecs
from la.symbol_table import LexemeTable, LexemeTableEntry



class LexicalException(Exception):
    def __init__(self, symbol, lineno, pos):
        self.args = ("Illegal character "+symbol+" at pos "+str(pos)+", line "+str(lineno),)
        self.symbol = symbol
        self.line = lineno
        self.pos = pos

# Since token_regex list create a set of global functions to
# define the regular expression for each token, 
# an instance may affect other instance token regex with same name.
# Before using another instance, call LexicalAnalyser.destroy().
# This will delete created token functions, literals and ignored characters from global definitions,
# preventing interaction with other instances.
class LexicalAnalyser:
    def __init__(self):
        self.token_regex = []
        self.literals = None
        self.ignore = None
        self.lexeme_table = None
        self.lexer = None
        self.ident = None

    global t_newline
    global t_error

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(t):
        pass

    #Token creator
    #PLY token precedence is in order of definition only for function definitions
    #I created this function to make easier to manage precedence for tokens that can be easily expressed with regex defitions
    def token_creator(self):
        global literals
        global tokens
        global t_ignore

        # Create literals and t_ignore variables in global scope
        # For PLY Lexer purposes 
        if(self.literals != None):
            literals = self.literals
        if(self.ignore != None):
            t_ignore = self.ignore

        token_list = [token for (token, regex) in self.token_regex]

        tokens = tuple(token_list)

        # Create t_TOKEN_NAME funcions in global scope
        # For PLY Lexer purposes 

        for (token, regex)  in self.token_regex:
            regex_func='def t_'+token+'(token):\n\tr\''+regex+'\'\n\treturn token'
            code=compile(regex_func,token,'exec')
            exec(code,globals())

    # Set string to analysed string
    # returning a Symbol Table
    def input(self, data):

        #create token list and funtions to be used by lexer
        self.token_creator()

        # Build the lexer
        self.lexer = lex.lex()

        # Give the lexer some input
        self.lexer.input(data)

        self.lexeme_table = LexemeTable(self.ident)

    # Save token to symbol table and also return it
    def token(self):
        try:
            token = self.lexer.token()
            if token: 
                self.lexeme_table.add_token(token.type, token.value, token.lineno, token.lexpos)
                return self.lexeme_table.last()
            else:
                return None
        except Exception as e:
            raise LexicalException(self.lexer.lexdata[self.lexer.lexpos],self.lexer.lineno, self.lexer.lexpos)

    # Deletes global token list, token functions, literals, and t_ignore
    def destroy(self):
        global tokens
        global literals
        global t_ignore
        for (token, regex)  in self.token_regex:
            del globals()["t_"+token]

        if 'tokens' in globals():
            del tokens
        if 'literals' in globals():
            del literals
        if 't_ignore' in globals():
            del t_ignore

    # Takes a line and separate into token name and regex string
    def line_to_token_regex(line):
        (token_name, regex) = line.split(" ",1)
        return (token_name, regex) 

    # Takes a file and separate its multiple lines into token list entries,
    # Handles 
    def file_to_token_list(self, file_path):
        token_regex = []

        f = open(file_path, "r")
        data = f.read().splitlines()

        token_regex = [LexicalAnalyser.line_to_token_regex(token) for token in data]

        f.close()

        self.token_regex = token_regex

        # Find "literals" entry in file
        literals_filter = list(filter(lambda t: t[0] == "literals", token_regex))
        # Remove from the token list, so a "literal" token is not created
        for lit in literals_filter:
            token_regex.remove(lit)
        # Saves only the first "literals" line
        if(len(literals_filter) > 0):
            self.literals = literals_filter[0][1]

        idents_filter = list(filter(lambda t: t[0] == "IDENT", token_regex))
        # Remove from the token list, so a "IDENT" token is not created
        for ident in idents_filter:
            token_regex.remove(ident)

        self.ident = idents_filter[0][1].split(" ")

        # Find "ignore" entry in file
        ignore_filter = list(filter(lambda t: t[0] == "ignore", token_regex))
        # Remove from the token list, so a "ignore" token is not created
        for ign in ignore_filter:
            token_regex.remove(ign)
        # Saves only the first "ignore" line
        if(len(ignore_filter) > 0):
            self.ignore = ignore_filter[0][1]

    #set token list from a tuple list
    def set_token_list(self, token_regex):
        self.destroy()
        self.token_regex = token_regex

    #load token definitions from file
    def from_file(self, file_path):
        self.destroy()
        self.file_to_token_list(file_path)