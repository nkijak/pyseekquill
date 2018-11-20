import sqlparse

class Parser(object):
  def parse(self, stream):
      stmts = sqlparse.parse(stream)
      return [self._visit(stmt) for stmt in stmts]

  def _visit(self, node):
    method_name = '_visit_' + type(node).__name__
    visitor = getattr(self, method_name, self._generic_visit)
    return visitor(node)

  def _generic_visit(self, node):
    print('No visit_{} method'.format(type(node).__name__))
    #raise Exception('No visit_{} method'.format(type(node).__name__))
