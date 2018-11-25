import pytest
from sqlparsing.ast_parser import ASTParser, Source

def test_removes_empty_stmts():
    with open('tests/resources/basic.sql') as input:
        actual = ASTParser().parse(input)

    assert len(actual) == 1

@pytest.mark.parametrize('input_path,expected_source', [
    ('tests/resources/basic.sql', {
        'a_table': Source('a_table'),
    }),
    ('tests/resources/easy_cte.sql', {
        'sub_table': Source('sub_table'), 
        'cte_table': Source('cte_table', is_cte=True),
    }),
    ('tests/resources/multi_cte.sql', {
        'sub_table': Source('sub_table'), 
        'cte_table': Source('cte_table', is_cte=True), 
        'other_table': Source('other_table', is_cte=True),
    }),
    ('tests/resources/join_simple.sql', {
        'f': Source('first_table'), 
        's': Source('second_table'),
    }),
    ('tests/resources/join_inner.sql', {
        'f': Source('first_table'), 
        's': Source('second_table'),
    }),
    ('tests/resources/join_outer.sql', {
        'f': Source('first_table'), 
        's': Source('second_table'),
    }),
    ('tests/resources/easy_union.sql', {
        'table_1': Source('table_1'), 
        'table_2': Source('table_2'),
    }),
    ('tests/resources/nested_cte.sql', {
        'outer_table': Source('outer_table', is_cte=True), 
        'first_inner': Source('first_inner', is_cte=True),
        'real_table_1': Source('real_table_1'),
    }),

])
def test_find_sources(input_path, expected_source):
    with open(input_path) as input:
        actual = ASTParser().parse(input)

    assert actual[0].source == expected_source

@pytest.mark.skip('too complex for now')
def test_complex_sources():
    with open('tests/resources/complex_1.sql') as input:
        actual = ASTParser().parse(input)

    assert actual[0].source == {
        'f': 'first_table', 
        's': 'second_table',
    }
