from sqlparsing.parser import Parser
from sqlparse import tokens, sql

class AST(object):
    def __init__(self):
        self.select = []
        self.table = {}
        self.order = {}
        self.in_select = False
        self.in_from = False
        self.in_with = False

class ASTParser(Parser):
    def __init__(self):
        self._asts = [] #use as stack
        self.sub_asts = []

    @property
    def asts(self):
        return self.sub_asts

    @property
    def ast(self):
        ''' get the current AST ie current context '''
        return self._asts[-1]

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
            self.ast.in_select = True
        elif node.ttype == tokens.Keyword.CTE and node.value.lower() == 'with':
            self.ast.in_with = True
        elif node.ttype == tokens.Keyword and \
          (node.value.lower() == 'from' or 'join' in node.value.lower()):
            self.ast.in_from = True
        pass

    def _visit_IdentifierList(self, node):
        print('visiting id list')
        for id in node.tokens:
            self._visit(id)

        if self.ast.in_select:
            self.ast.in_select = False


    def _visit_Identifier(self, node):
        print('visiting id -- in_select?{} in_from?{} in_with?{}'.format(self.ast.in_select, self.ast.in_from, self.ast.in_with))
        print('id name={} alias={}'.format(node.get_real_name(), node.get_alias()))
        if self.ast.in_select:
            self.ast.select.append(node.get_name())
        elif self.ast.in_from:
            self.ast.table[node.get_name()] = node.get_real_name()
            self.ast.in_from = False
        elif self.ast.in_with:
            self.ast.table[node.get_name()] = node.get_real_name()
            self._asts.append(AST())
            for t in node.tokens:
              self._visit(t)
        else:
            print('found ids {} but not sure what for'.format(node.get_name()))

    def _visit_Parenthesis(self, node):
        print('visiting paren')
        for id in node.tokens:
            self._visit(id)
        self.sub_asts.append(self._asts.pop())
        


