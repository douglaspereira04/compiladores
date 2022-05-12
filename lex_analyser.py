

# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex


#Since token_regex list create a set of global functions to
#define the regular expression for each token, 
#an instance may affect other instance token regex with same name
#Before using another instance, call LexicalAnalyser.destroy
class LexicalAnalyser:
    def __init__(self, token_regex):
        self.token_regex = token_regex
    # A string containing ignored characters (spaces and tabs)
    global t_ignore
    t_ignore  = ' \t'

    global t_newline
    global t_error

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


    #Token creator
    #PLY token precedence is in order of definition only for function definitions
    #I created this function to make easier to manage precedence for tokens that can be easily expressed with regex defitions
    def token_creator(self):
        global tokens
        token_list = [token for (token, regex) in self.token_regex]

        tokens = tuple(token_list)

        for (token, regex)  in self.token_regex:
            regex_func='def t_'+token+'(token):\n\tr\''+str(regex)+'\'\n\treturn token'
            code=compile(regex_func,token,'exec')
            exec(code,globals())

    def analysis(self, data):

        #create token list and funtions to be used by lexer
        self.token_creator()

        # Build the lexer
        lexer = lex.lex()

        # Give the lexer some input
        lexer.input(data)

        
        # Tokenize
        while True:
            tok = lexer.token()
            if not tok: 
                break      # No more input 
            print(tok)

    #del global token list and remove token function namespaces
    def destroy(self):
        global tokens
        for (token, regex)  in self.token_regex:
            del globals()["t_"+token]
        del tokens




# Test it out
data = '''
    def break jef agua "agua" agua 3 + 4 * 10
    + -20 *2
'''

if __name__ == "__main__":

    #List of tokens and regex
    token_regex = [
        ("DEF",r'def'),
        ("BREAK",r'break'),
        ("IDENT",r'(([a-z]|[A-Z])+)'),
        ("INT",r'[0-9]+'),
        ("FLOAT",r'[0-9]+.\..[0-9]+'),
        ("STRING",r'\".*\"'),
        ("PLUS",r'\+'),
        ("MINUS",r'-'),
        ("DIVIDE",r'\\'),
        ("TIMES",r'\*'),
        ("RELOP",r'(<|>|<=|>=|==)')
    ]

    la = LexicalAnalyser(token_regex)
    la.analysis(data)

