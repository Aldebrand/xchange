import click

from operations import config as ops_config


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
    success_msg, error_msg = ops_config.base_commission(commission)

    if error_msg:
        click.secho(error_msg, fg='red', bold=True, err=True)
        click.get_current_context().exit(1)

    click.secho(success_msg, fg='green')
