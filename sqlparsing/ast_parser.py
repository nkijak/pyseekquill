from sqlparsing.parser import Parser
from sqlparse import tokens, sql

class AST(object):
    def __init__(self):
        self.select = []
        self.table = []
        self.order = {}

class ASTParser(Parser):
    def __init__(self):
        self._asts = [] #use as stack
        self.in_select = False
        self.in_from = False
        self.in_with = False
        self.sub_asts = []

    @property
    def asts(self):
      return self.sub_asts

    def _visit_Statement(self, node):
        self._asts.append(AST())
        print('visiting statement')
        for token in node.tokens:
            self._visit(token)

        self.sub_asts += self._asts
        self._asts = []
        return self.asts

    def _visit_Operation(self, node):
        print('visiting operation')
        pass

    def _visit_Token(self, node):
        print('visiting token {} {}'.format(node.ttype, node.value.lower()))
        if node.ttype == tokens.Keyword.DML and node.value.lower() == 'select':
            self.in_select = True
        elif node.ttype == tokens.Keyword.CTE and node.value.lower() == 'with':
            self.in_with = True
        elif node.ttype == tokens.Keyword and node.value.lower() == 'from':
            self.in_from = True
        pass

    def _visit_IdentifierList(self, node):
        print('visiting id list')
        for id in node.tokens:
            self._visit(id)

        if self.in_select:
            self.in_select = False


    def _visit_Identifier(self, node):
        print('visiting id -- in_select?{} in_from?{} in_with?{}'.format(self.in_select, self.in_from, self.in_with))
        print('id name={} alias={}'.format(node.get_name(), node.get_alias()))
        names = [t.value for t in node.tokens]
        ast = self._asts[-1]
        if self.in_select:
            ast.select = ast.select + names
        elif self.in_from:
            ast.table = ast.table + names
            self.in_from = False
        elif self.in_with:
            ast.table.append(node.get_name())
            self._asts.append(AST())
            for t in node.tokens:
              self._visit(t)
        else:
            print('found ids {} but not sure what for'.format(names))

    def _visit_Parenthesis(self, node):
        print('visiting paren')
        for id in node.tokens:
            self._visit(id)
        self.sub_asts.append(self._asts.pop())
        


