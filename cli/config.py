import click

from cli.utils import load_config, update_config


@click.group()
def config():
    """Command for editing the cli configuration."""
    pass


@config.command()
@click.argument('commission', type=float, required=True)
def base_commission(commission):
    """
    Replace the default commmission with the new specified commission.

    \b
    COMMISSION - new commission
    """
    config = load_config()
    config['base_commission'] = commission

    try:
        update_config(config=config)
    except Exception as e:
        msg = f'The following error has been occurred: {e}'
        click.secho(msg, fg='red', bold=True, err=True)
        click.get_current_context().exit(1)
