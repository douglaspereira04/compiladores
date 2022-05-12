

# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

tokens = None

#Token creator
#PLY token precedence is in order of definition only for function definitions
#I created this function to make easier to manage precedence for tokens that can be easily expressed with regex defitions
def token_creator(token_regex):
    global tokens
    token_list = [token for (token, regex) in token_regex]

    tokens = tuple(token_list)

    for (token, regex)  in token_regex:
        regex_func='def t_'+token+'(token):\n\tr\''+str(regex)+'\'\n\treturn token'
        code=compile(regex_func,token,'exec')
        exec(code,globals())

#List of tokens and regex
token_regex = [
    ("DEF",r'def'),
    ("BREAK",r'break'),
    ("IDENT",r'(([a-z]|[A-Z])+)'),
    ("INT",r'[0-9]+'),
    ("FLOAT",r'[0-9]+.\..[0-9]+'),
    ("STRING",r'\".*\"'),
    ("PLUS",r'-'),
    ("MINUS",r'-'),
    ("DIVIDE",r'-'),
    ("RELOP",r'(<|>|<=|>=|==)')
]

#create token list and funtions to be used by lexer
token_creator(token_regex)

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# Test it out
data = '''
    def break jef agua "agua" agua 3 + 4 * 10
    + -20 *2
'''

if __name__ == "__main__":


    # Give the lexer some input
    lexer.input(data)

    
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input 
        print(tok)


