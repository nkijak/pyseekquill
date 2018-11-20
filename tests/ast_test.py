import pytest
from sqlparsing.ast_parser import ASTParser

def test_basic():
    with open('tests/resources/basic.sql') as input:
        actual = ASTParser().parse(input)

    assert actual[0].ast.table == ['a_table']

