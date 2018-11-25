import pytest
from sqlparsing.ast_parser import ASTParser, Source

def test_removes_empty_stmts():
    with open('tests/resources/basic.sql') as input:
        actual = ASTParser().parse(input)

    assert len(actual) == 1

def test_basic_sources():
    with open('tests/resources/basic.sql') as input:
        actual = ASTParser().parse(input)

    assert actual[0].source == {
        'a_table': Source('a_table'),
    }

def test_easy_cte_sources():
    with open('tests/resources/easy_cte.sql') as input:
        actual = ASTParser().parse(input)

    assert actual[0].source == {
        'sub_table': Source('sub_table'), 
        'cte_table': Source('cte_table', is_cte=True),
    }

def test_multi_cte_sources():
    with open('tests/resources/multi_cte.sql') as input:
        actual = ASTParser().parse(input)

    #FIXME how to deal with subqueries of same table with different aliases
    assert actual[0].source == {
        'sub_table': Source('sub_table'), 
        'cte_table': Source('cte_table', is_cte=True), 
        'other_table': Source('other_table', is_cte=True),
    }

@pytest.mark.parametrize('file_name', [
        ('join_simple.sql'),
        ('join_inner.sql'),
        ('join_outer.sql'),
    ])
def test_join_sources(file_name):
    with open('tests/resources/'+file_name) as input:
        actual = ASTParser().parse(input)

    assert actual[0].source == {
        'f': Source('first_table'), 
        's': Source('second_table'),
    }

@pytest.mark.skip('too complex for now')
def test_complex_sources():
    with open('tests/resources/complex_1.sql') as input:
        actual = ASTParser().parse(input)

    assert actual[0].source == {
        'f': 'first_table', 
        's': 'second_table',
    }
