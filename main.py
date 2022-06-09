# Douglas Pereira Luiz

from la.lex_analyser import LexicalAnalyser, LexicalException
from sa.ll1_parser import LL1Parser
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
                print(parent.name, end="")
            else:
                print(parent.name)
        if parent == None:
            return
        if(len(parent.children)>0):
            for child in parent.children[:-1]:
                print(indent + "├" + "─" * indent_width, end="")
                _ptree(start, child, tree, parent, indent + "│" + " " * 4)
                
            child = parent.children[-1]
            print(indent + "└" + "─" * indent_width, end="")
            _ptree(start, child, tree, parent, indent + " " * 5)  # 4 -> 5
    
    print(tree.name)
    _ptree(tree, tree, tree)


# First command line argument is tokens file path
# Second command line argument is path of file with code to be analysed
# Third command line argument is path of output file
if __name__ == "__main__":
    output_path = None
    token_file = None
    data_file = None
    grammar_file = None

    if(len(sys.argv)==4):
        [_, token_file, grammar_file, data_file] = sys.argv 
    else:
        [_, token_file, grammar_file, data_file, output_path] = sys.argv 

    data = read_file(data_file)

    grammar = read_file(grammar_file)

    la = LexicalAnalyser()
    la.from_file(token_file)
    la.input(data)

    try:
        while True:
            token = la.token()
            if (not token):
                break #no more tokens
    except LexicalException as e:
        print(e)
    else:
        lexeme_table = la.lexeme_table
        if(output_path):
            write_file(output_path,lexeme_table.to_string()+"\n"+lexeme_table.to_symbol_table_string())
        else:
            #print(lexeme_table.to_string())
            #print(lexeme_table.to_symbol_table_string())

            ll1_parser = LL1Parser(grammar)
            result = ll1_parser.parse(lexeme_table.get_token_list(), 1000000000)
            print(result.accepted)
            ptree(result.tree.children[0])



