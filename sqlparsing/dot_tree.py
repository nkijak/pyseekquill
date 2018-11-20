import sqlparse
import sys

graph_start = '''
digraph astgraph {
  node [shape=none, fontsize=10, fontname="Courier", height=.1];
  ranksep=.3;
  edge [arrowsize=.5]
'''


def render(stmt, nodes, edges, root=None):
    if stmt.ttype in [
            sqlparse.tokens.Whitespace.Newline,
            sqlparse.tokens.Whitespace,
            sqlparse.tokens.Punctuation]:
        return
    node_name = 'node{}'.format(len(nodes))
    if root:
        edges.append('{} -> {}'.format(root, node_name))
    if stmt.is_group: #isinstance(stmt, sqlparse.sql.Statement):
        value = 'stmt'
    else:
        value = stmt.value.replace('\n', ' ')
    nodes.append('{} [ label="{}\\n{}\\n{}" ]'.format(node_name, value, stmt.ttype, type(stmt).__name__))
    if stmt.is_group:
        children = [render(i, nodes, edges, node_name) for i in stmt.tokens]
        for child in children:
            if child:
                edges.append('{} -> {}'.format(node_name, child))
    else:
        return node_name

def to_dot(stream):
    nodes = []
    edges = []
    for stmt in sqlparse.parse(stream):
        render(stmt, nodes, edges)
    return '{}\n{}\n{}\n}}'.format(
            graph_start,
            '\n'.join(nodes),
            '\n'.join(edges))


if __name__ == '__main__':
    with open(sys.argv[1]) as input:
        with open('output.dot', 'w') as output:
            output.write(to_dot(input))

