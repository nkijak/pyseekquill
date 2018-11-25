from functools import reduce
from sqlparsing.parser import Parser
from sqlparse import tokens, sql

class BaseObject(object):
    def __eq__(self, other):
      if not isinstance(other, type(self)):
        return False
      return self.__dict__ == other.__dict__

    def __repr__(self):
      return self.__dict__.__str__()

class Source(BaseObject):
    ''' data object for a data source eg table '''
    def __init__(self, name, is_cte=False):
      self.name = name
      self.is_cte = is_cte


class AST(BaseObject):
    def __init__(self, select=None, source=None, order=None):
        self.select = select if select else []
        self.source = source if source else {}
        self.order = order if order else {}
        self.in_select = False
        self.in_from = False
        self.in_with = False

    def __bool__(self):
        return len(self.source if self.source else {}) > 0

    def merge(self, other):
      retval = AST(select=self.select + other.select, 
                   source=other.source, 
                   order=other.order)
      retval.source.update(self.source)
      retval.order.update(self.order)
      return retval

from pprint import pprint
class ASTParser(Parser):
    def __init__(self):
        self._asts = [] #use as stack
        self.sub_asts = []

    @property
    def ast(self):
        ''' get the current AST ie current context '''
        return self._asts[-1]

    def _visit_Statement(self, node):
        self._asts.append(AST())
        print('visiting statement')
        for token in node.tokens:
            self._visit(token)

        print('reducing...')
        asts = self.sub_asts + self._asts
        pprint(asts)
        retval = reduce(lambda el, acc: acc.merge(el), asts)
        self._asts = []
        self.sub_asts = []

        print('reduced to:')
        pprint(retval)

        return retval

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


    def _visit_IdentifierList(self, node):
        print('visiting id list')
        for id in node.tokens:
            self._visit(id)

        if self.ast.in_select:
            self.ast.in_select = False


    def _visit_Identifier(self, node):
        print('visiting id name={} alias={} -- in_select?{} in_from?{} in_with?{}'.format(
          node.get_real_name(), 
          node.get_alias(), 
          self.ast.in_select, 
          self.ast.in_from, 
          self.ast.in_with))
        if self.ast.in_select:
            self.ast.select.append(node.get_name())

        elif self.ast.in_from:
            print('-- identified source {}'.format(node.get_name()))
            self.ast.source[node.get_name()] = Source(node.get_real_name())
            self.ast.in_from = False

        elif self.ast.in_with:
            print('-- new ast for {}'.format(node.get_name()))
            self.ast.source[node.get_name()] = Source(node.get_real_name(), is_cte=True)
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
        print('-- exiting parens:')
        pprint(self.sub_asts)
        pprint(self._asts)
        


