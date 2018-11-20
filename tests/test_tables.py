import pytest
from sqlparsing.table_parser import TableParser

@pytest.mark.skip(reason='not ready for this')
def test_easy_table():
    expected = ['table']
    with open('tests/resources/basic.sql') as basic:
        actual = TableParser().parse(basic)
    assert actual == expected
