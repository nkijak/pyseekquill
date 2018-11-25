from sqlparsing.ast_parser import AST

def test_truthyness():
    true = AST()
    true.source = {'test': 'this'}
    false = AST()

    assert true
    assert not false
