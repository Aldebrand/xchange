import click

from cli.config import config
from cli.exchange import exchange
from cli.loan import end_loan, loan
from operations import utils


@click.group(invoke_without_command=True)
def cli():
    utils.init_db()


cli.add_command(exchange)
cli.add_command(config)
cli.add_command(loan)
cli.add_command(end_loan)

if __name__ == '__main__':
    cli()
