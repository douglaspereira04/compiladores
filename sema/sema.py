from texttable.texttable import Texttable

class SemanticException(Exception):
    def __init__(self, symbol, lineno, pos):
        self.args = ("Unexpected symbol "+symbol+" at pos "+str(pos)+", line "+str(lineno),)
        self.symbol = symbol
        self.line = lineno
        self.pos = pos

class NoLoopBreakException(SemanticException):
    def __init__(self, lineno, pos):
        super().__init__("break", lineno, pos)
        self.args = ("Unexpected break at pos "+str(pos)+", line "+str(lineno),)

class RedeclarationException(SemanticException):
    def __init__(self, symbol, lineno, pos, other_line, other_pos):
        super().__init__(symbol, lineno, pos)
        self.args = ("Redeclaration of "+symbol+" at pos "+str(pos)+", line "+str(lineno)+" already declared at pos "+str(other_pos)+", line "+str(other_line),)

class IncompatibleOperandsException(SemanticException):
    def __init__(self, next_lexeme, lineno, pos):
        super().__init__(next_lexeme, lineno, pos)
        self.args = ("Incompatible operands in expression next to "+next_lexeme+" at pos "+str(pos)+", line "+str(lineno),)


class SymbolTable:
    def __init__(self,node, parent, is_loop):
        if(node == None):
            self.lexeme = "GLOBAL"
            self.line = 0
            self.pos = 0
        else:
            self.lexeme = node.lexeme()
            self.line = node.line
            self.pos = node.pos

        self.parent = parent
        self.children = []
        if(self.parent != None):
            self.parent.children.append(self)

        self.is_loop = is_loop

        self.symbols = list()

    def get_type(self, lexeme):
        for symbol in self.symbols:
            if(symbol[1] == lexeme):
                return symbol[4]
        return None

    def add_func(self, node, param_count):
        self.assert_unique(node)
        """SYMBOL, LEXEME, LINE, POS, TYPE, PARAM_COUNT"""
        self.symbols.append([node.symbol(), node.lexeme(), node.line, node.pos, "func", param_count])

    def add_var(self, var_type, node):
        self.assert_unique(node)
        """SYMBOL, LEXEME, LINE, POS, TYPE, PARAM_COUNT"""
        self.symbols.append([node.symbol(), node.lexeme(), node.line, node.pos, var_type, 0])

    def assert_unique(self, node):
        for symbol in self.symbols:
            if(node.lexeme() == symbol[1]):
                raise RedeclarationException(node.symbol(), node.line, node.pos, symbol[2], symbol[3])

    def to_text(self):
        table = Texttable()
        rows = [["SÍMBOLOS", "LEXEMA", "LINHA", "POS", "TIPO", "PARAMETROS"]] + self.symbols
        table.add_rows(rows)
        inicio = "INICIO: [ LEXEMA: "+str(self.lexeme)+"; LINHA: "+str(self.line)+"; POSIÇÂO: "+str(self.pos)+"]"
        parent = self.parent
        parent = "PAI IMEDIATO: [ LEXEMA: "+str(parent.lexeme)+"; LINHA: "+str(parent.line)+"; POSIÇÂO: "+str(parent.pos)+"]"
        return inicio+"\n"+parent+"\n"+table.draw()

    def is_empty(self):
        return len(self.symbols)==0

class ExpressionNode:

    def __init__(self, value, value_type, left, right):
        self.value = value
        self.value_type = value_type
        self.signal = None
        self.children = []
        self.parent = None
        if(left != None):
            self.children.append(left)
            left.parent = self
        if(right != None):
            self.children.append(right)
            right.parent = self

    def set_signal(self, signal):
        self.signal = signal



class SemanticAnalyser:
    def __init__(self, grammar):
        self.grammar = grammar

    def get_symbol_table(self):
        global curr_table
        table = curr_table
        while(table.parent != None):
            table = table.parent

        return table

    def put(self,node):

        """
        Podemos executar as ações que precedem à derivação do símbolo a seguir (símbolo que está em node)
        """
        if(not (node.do_before() is None)):
            self.do(node, node.do_before())

        if(node.is_last() and node.is_terminal()):
            """
            Aqui sabemos que é o símbolo terminal no fim da cauda de uma produção
            Então podemos executar as ações que o sucedem
            """
            if(not (node.do_after() is None)):
                self.do(node, node.do_after())
            """
            Além disso, a leitura desse símbolo provoca a subida na árvore de derivações
            Por isso, fazemos o que vem a seguir:
            """
            parent = node.parent
            while(parent.is_last()):
                """
                Se parent, o não terminal que derivou o símbolo do nó atual, 
                estiver no fim da cauda da produção que o derivou, 
                podemos executar a ação que o sucede
                """

                if(not (parent.do_after() is None)):
                    self.do(parent, parent.do_after())
                """
                Equanto sucessivamente o pai desse pai também estiver no fim da cauda 
                de uma produção, sucessivamente haverão subidas na árvore,
                e sucessivamente também deverá ser executada as ações que sucedem 
                esses não terminais
                """
                parent = parent.parent



    def do(self, node, commands):
        if(commands != None):
            command = ""
            for symbol in commands.split(" "):
                if(symbol.startswith("#") and symbol.endswith("#")):
                    """
                    Quando um símbolo em uma ação está entre "#" ele é considerado um atributo
                    do nó da árvore. Então, para modificar ou usar atributos de símbolos de uma produção
                    devemos dispor o atributo entre "#".
                    Exemplo: A -> § #B_0.valor# = 2 § B c

                    B_0 indica que é o primeiro B da produção de A.
                    O número depois de "_" é uma marcação para caso de repetição.
                    Ou seja, se anotarmos símbolo na forma S_n, estamos nos referindo
                    ao enésimo S da produção, incluindo a cabeça.
                    Não pode ser omitido.
                    """
                    symbol_attribute = symbol[1:-1]
                    attribute = None
                    if(len(symbol_attribute.split("."))>1):
                        (symbol, attribute) = symbol_attribute.split(".")
                    else:
                        symbol = symbol_attribute

                    (symbol,index) = symbol.rsplit("_",1)
                    index = int(index)
                    target = None
                    if(symbol == node.derived_from().head() and index == 0):
                        #refere-se à cabeça da produção
                        target = "node.parent"
                    else:
                        #referese à um irmão ou a sí mesmo
                        target = "node.sibling(\""+symbol+"\","+str(index)+")"

                    if(attribute != None):
                        symbol = target+".attributes[\""+ attribute +"\"]"
                    else:
                        symbol = target

                command = command + symbol + " "
            exec(command)

curr_table = None

def scope(node = None, is_loop = False):
    global curr_table
    curr_table = SymbolTable(node, curr_table, is_loop)

def unscope():
    global curr_table
    curr_table = curr_table.parent


def add_func(node, param_count):
    curr_table.add_func(node, param_count)

def add_var(var_type, node):
    curr_table.add_var(var_type, node)

def assertLoop(node):
    global curr_table
    table = curr_table 
    while(table != None):
        if(table.is_loop):
            return True
        table = table.parent

    raise NoLoopBreakException(node.line, node.pos)

def get_ident_type(lexeme):
    global curr_table
    table = curr_table

    while(table != None):
        ident_type = table.get_type(lexeme)
        if(ident_type != None):
            return ident_type

        table = table.parent

    return None


def exp_node(value, value_type, left=None, right=None, indexes=None):
    return ExpressionNode(value, value_type, left, right)

"""
tree printer from https://stackoverflow.com/questions/51903172/how-to-display-a-tree-in-python-similar-to-msdos-tree-command
"""
def exp_ptree(tree, indent_width=1):

    def _exp_ptree(start, parent, tree, grandpa=None, indent=""):
        if parent != start:
            if parent.parent is None:  # Ask grandpa kids!
                if(parent.signal != None):
                    print(" "+str(parent.signal) +str(parent.value), end="")
                else:
                    print(" "+str(parent.value), end="")
            else:
                if(parent.signal != None):
                    print(" "+str(parent.signal) +str(parent.value))
                else:
                    print(" "+str(parent.value))

        if parent == None:
            return
        if(len(parent.children)>0):
            for child in parent.children[:-1]:
                print(indent + "├" + "─" * indent_width, end="")
                _exp_ptree(start, child, tree, parent, indent + "│" + " " * 4)
                
            child = parent.children[-1]
            print(indent + "└" + "─" * indent_width, end="")
            _exp_ptree(start, child, tree, parent, indent + " " * 5)  # 4 -> 5
    
    if(tree.signal != None):
        print(str(tree.signal) +str(tree.value))
    else:
        print(str(tree.value))

    _exp_ptree(tree, tree, tree)

def set_signal(exp_node, signal):
    exp_node.set_signal(signal)

def append(atribute, value):
    atribute.append(value)

def assert_expression(exp_root, terminal_associated=None):
    stack = [exp_root]

    value_type = None
    while(len(stack)>0):
        node = stack.pop()
        if(node.value_type == "op"):
            for child in node.children:
                stack.append(child)
        else:
            if(value_type == None):
                value_type = node.value_type
            else:
                if(value_type != node.value_type):
                    raise IncompatibleOperandsException(terminal_associated.lexeme(), terminal_associated.line, terminal_associated.pos)

    print("\nEXPRESSÃO A SEGUIR DE \""+terminal_associated.lexeme()+"\" LINHA: "+str(terminal_associated.line)+"; POS:"+str(terminal_associated.pos))
    exp_ptree(exp_root)


