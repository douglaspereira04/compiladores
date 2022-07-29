# Douglas Pereira Luiz

from la.lex_analyser import LexicalAnalyser, LexicalException, Token
from sa.ll1_parser import LL1Parser, SyntaxException
from sema.sema import SemanticAnalyser
from sa.grammar import Grammar
import sys


def read_file(file_path):
    f = open(file_path, "r")
    data = f.read() 
    f.close()
    return data

def write_file(file_path, string):
    f = open(file_path, "w")
    f.write(string)
    f.close()


"""
tree printer from https://stackoverflow.com/questions/51903172/how-to-display-a-tree-in-python-similar-to-msdos-tree-command
"""
def ptree(tree, indent_width=1):

    def _ptree(start, parent, tree, grandpa=None, indent=""):
        if parent != start:
            if parent.parent is None:  # Ask grandpa kids!
                if(parent.is_terminal()):
                    print(parent.derived_from()+":"+parent.symbol()+":"+parent.lexeme(), end="")
                else:
                    print(parent.derived_from()+":"+parent.symbol(), end="")
            else:
                if(parent.is_terminal()):
                    print(parent.derived_from()+":"+parent.symbol()+":"+parent.lexeme())
                else:
                    print(parent.derived_from()+":"+parent.symbol())
        if parent == None:
            return
        if(len(parent.children)>0):
            for child in parent.children[:-1]:
                print(indent + "├" + "─" * indent_width, end="")
                _ptree(start, child, tree, parent, indent + "│" + " " * 4)
                
            child = parent.children[-1]
            print(indent + "└" + "─" * indent_width, end="")
            _ptree(start, child, tree, parent, indent + " " * 5)  # 4 -> 5
    
    print(tree.symbol())
    _ptree(tree, tree, tree)

def p_symbol_tables(symbol_tables):
    if(not symbol_tables.is_empty()):
        print("\n"+symbol_tables.to_text())
    for child in symbol_tables.children:
        p_symbol_tables(child)

def lasa(token_file, grammar_file, data_file, output_path):
    MAX = 1000000
    data = read_file(data_file)

    grammar_text = read_file(grammar_file)
    grammar_text = read_file(grammar_file)


    try:
        grammar = Grammar(grammar_text)
        la = LexicalAnalyser()
        ll1_parser = LL1Parser(grammar)
        sema = SemanticAnalyser(grammar)
   
        la.from_file(token_file)
        la.input(data)
        while True:
            token = la.token()
            if (not (token is None)):

                i = 0
                while((i < MAX) and (1 < len(ll1_parser.stack))):
                    (must_break, node) = ll1_parser.parse(token)
                    #node is current node being visited in parsing tree
                    if(node != None):
                        sema.put(node)
                    if(must_break):
                        break

                    i+=1
            else:
                while(len(ll1_parser.parents)>0):
                    (must_break, node) = ll1_parser.parse()
                    if(node != None):
                            sema.put(node)
                #ptree(ll1_parser.tree.children[0])
                break #no more tokens

        symbol_table = sema.get_symbol_table()

        p_symbol_tables(symbol_table)

        print("As expressões aritiméticas são válidas;")
        print("Todo break está no escopo de um for;")
        print("As expressões aritiméticas são válidas;")
    except Exception as e:
        print(e)


# First command line argument is tokens file path
# Second command line argument is path of file with code to be analysed
# Third command line argument is path of output file
if __name__ == "__main__":
    output_path = None
    token_file = None
    data_file = None
    grammar_file = None
    is_sa = False

    if("sa" in sys.argv):
        grammar_file = "resources/grammar"
        [_, data_file,_] = sys.argv 
        is_sa = True

    elif(len(sys.argv)==2):
        grammar_file = "resources/grammar"
        token_file = "resources/tokens"
        [_, data_file] = sys.argv 
    elif(len(sys.argv)==4):
        [_, token_file, grammar_file, data_file] = sys.argv 
    else:
        [_, token_file, grammar_file, data_file, output_path] = sys.argv 

    if( not is_sa):
        lasa(token_file, grammar_file, data_file, output_path)




