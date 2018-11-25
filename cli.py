import click
from sqlparsing.ast_parser import ASTParser


@click.command()
@click.argument('queryfile', type=click.File('r'))
def tables(queryfile):
    query = queryfile.read()
    results = ASTParser().parse(query)
    click.echo('There were {} statement(s) in {}'.format(len(results), queryfile.name))
    for r in results:
        names = [t.name for t in r.source.values() if not t.is_cte]
        click.echo('Dependant tables:\n{}'.format('\n'.join(names)))

if __name__ == '__main__':
    tables()
