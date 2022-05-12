

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
    def __init__(self):
        self.token_regex = []
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
        if 'tokens' in globals():
            del tokens

    def line_to_token_regex(line):
        (token_name, regex) = line.split(":")
        return (token_name, regex) 

    def file_to_token_list(file_path):
        token_regex = []

        f = open(file_path, "r")
        data = f.read().splitlines()

        token_regex = [LexicalAnalyser.line_to_token_regex(token) for token in data]

        f.close()
        return token_regex

    def set_token_list(self, token_regex):
        self.destroy()
        self.token_regex = token_regex

    def from_file(self, file_path):
        self.destroy()
        self.token_regex = LexicalAnalyser.file_to_token_list(file_path)