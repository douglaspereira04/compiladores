
class Node:
    def __init__(self, symbol, lexeme, global_variables, parent=None):
        self._symbol = symbol
        self.parent = parent
        self.children = []
        self._lexeme = lexeme

        self.children_attributes = dict()
        self.global_variables = global_variables

        if parent:
            self.parent.children.append(self)

    def produces(self):
        if(self.is_terminal()):
            return None
        else:
            products = ""
            for product in self.children:
                products = products + product._symbol + " "

            products = products.strip()

            return self._symbol + " -> " + products

    def derived_from(self):
        return self.parent.produces()

    def symbol(self):
        return self._symbol

    def lexeme(self):
        return self._lexeme

    def is_terminal(self):
        if(len(self.children)>0):
            return False
        return True

    def get_childreen_attribute(self, symbol, attr):
        return self.children_attributes[symbol][attr]

    def set_childreen_attribute(self, symbol, attr, value):
        self.children_attributes[symbol][attr] = value

    def get_attribute(self, attr):
        return self.parent.children_attributes[self.name][attr]

    def set_attribute(self, attr, value):
        self.parent.children_attributes[self.name][attr] = value

    def get_global_variable(self, variable):
        return self.global_variables[variable]

    def set_global_variable(self, variable, value):
        self.global_variables[variable] = value

