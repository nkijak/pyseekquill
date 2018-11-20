class StrInterpreter(object):
  def visit_str(self, node):
    print('visiting str')

class IntInterpreter(object):
  def visit_int(self, node):
    print('visiting int')

class NodeVisitor(StrInterpreter, IntInterpreter):
  def visit(self, node):
    method_name = 'visit_' + type(node).__name__
    visitor = getattr(self, method_name, self.generic_visit)
    return visitor(node)

  def generic_visit(self, node):
    raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(StrInterpreter, IntInterpreter):
  def __init__(self):
    print('ready')
    

if __name__ == '__main__':
  i = NodeVisitor()
  i.visit('str')
  i.visit(1)
  i.visit(2.9)
