import pytest
from sqlparsing.ast_parser import ASTParser

def test_basic_tables():
    with open('tests/resources/basic.sql') as input:
        actual = ASTParser().parse(input)

    assert actual[0][0].table == ['a_table']

def test_easy_cte_tables():
    with open('tests/resources/easy_cte.sql') as input:
        actual = ASTParser().parse(input)

    actual_tables = []
    for t in [a.table for a in actual[0]]:
        actual_tables = actual_tables + t
    assert actual_tables == ['sub_table', 'cte_table']

def test_multi_cte_tables():
    with open('tests/resources/multi_cte.sql') as input:
        actual = ASTParser().parse(input)

    actual_tables = []
    for t in [a.table for a in actual[0]]:
        actual_tables += t
    #FIXME gets all the table referernces, but allows multiples
    assert actual_tables == ['sub_table', 'cte_table', 'cte_table', 'other_table']

@pytest.mark.parametrize('file_name', [
        ('join_simple.sql'),
        ('join_inner.sql'),
        ('join_outer.sql'),
    ])
def test_join_tables(file_name):
    with open('tests/resources/'+file_name) as input:
        actual = ASTParser().parse(input)

    actual_tables = []
    for t in [a.table for a in actual[0]]:
        actual_tables += t
    assert actual_tables == ['first_table', 'second_table']
