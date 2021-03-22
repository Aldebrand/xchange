import click

from operations import exchange as ops_exchange


@click.command()
@click.argument('amount', type=float, required=True)
@click.argument('origin-currency', type=str, required=True)
@click.argument('target-currency', type=str, required=True, default='EUR')
def exchange(amount: int, origin_currency: str, target_currency: str):
    """
    Exchange a certain amount of money from one currency to another.

    \b
    AMOUNT - the amount of money to exchange
    ORIGIN_CURRENCY - original currency
    TARGET_CURRENCY - target currency (defaults to EUR)
    """
    success_msg, error_msg = ops_exchange.exchange(amount, origin_currency,
                                                   target_currency)

    if error_msg:
        click.secho(error_msg, fg='red', bold=True, err=True)
        click.get_current_context().exit(1)

    click.secho(success_msg, fg='green')
