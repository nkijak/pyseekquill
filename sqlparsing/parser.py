import sqlparse
import logging

class Parser(object):
  def parse(self, stream):
      stmts = sqlparse.parse(stream)
      return [result for result in [self._visit(stmt) for stmt in stmts] if result]

  def _visit(self, node):
    method_name = '_visit_' + type(node).__name__
    visitor = getattr(self, method_name, self._generic_visit)
    return visitor(node)

  def _generic_visit(self, node):
    logging.warning('No visit_{} method'.format(type(node).__name__))
    #raise Exception('No visit_{} method'.format(type(node).__name__))
