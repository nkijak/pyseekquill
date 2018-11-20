from sqlparsing.parser import Parser
from sqlparse import tokens, sql

class AST(object):
    def __init__(self):
        self.select = []
        self.table = []
        self.order = {}

class ASTParser(Parser):
    def __init__(self):
        self.ast = None
        self.in_select = False
        self.in_from = False

    def _visit_Statement(self, node):
        self.ast = AST()
        for token in node.tokens:
            self._visit(token)
        return self

    def _visit_Operation(self, node):
        pass

    def _visit_Token(self, node):
        if node.ttype == tokens.Keyword.DML and node.value.lower == 'select':
            self.in_select = True
        if node.ttype == tokens.Keyword and node.value.lower == 'from':
            self.in_from = True
        pass

    def _visit_IdentifierList(self, node):
        for id in node.tokens:
            self._visit(id)

    def _visit_Identifier(self, node):
        names = [t.value for t in node.tokens]
        if self.in_select:
            self.select = self.select + names
            self.in_select = False
        if self.in_from:
            self.table = self.table + names
            self.in_from = False
        else:
            print('found ids {} but not sure what for'.format(names))



