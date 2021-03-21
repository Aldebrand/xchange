import click

from cli.config import config
from cli.exchange import exchange
from cli.loan import end_loan, loan
from cli.utils import init_mongo_client, load_config, update_config


def _init_db():
    """
    Initialize a database.
    """
    config = load_config()
    db_config = config['db']
    do_init = db_config['init_db']

    if do_init:
        client = init_mongo_client()
        db = client['xchange']
        db.create_collection('loans')
        config['db']['init_db'] = False
        update_config(config=config)
        client.close()


@click.group(invoke_without_command=True)
def cli():
    _init_db()


cli.add_command(exchange)
cli.add_command(config)
cli.add_command(loan)
cli.add_command(end_loan)

if __name__ == '__main__':
    cli()
