from sqlparsing.parser import Parser

class TableParser(Parser):
    def _visit_Statement(self, node):
        for token in node.tokens:
            return self._visit(token)

    def _visit_Operation(self, node):
        return node.value

    def _visit_Token(self, node):
        return node.value
