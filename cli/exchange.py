import click

from cli.utils import convert_money, load_config


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
    # Load the configuration before exchanging the money in order to exchange
    # it with the right commission.
    # If something went wrong, exit the cli.
    config = load_config()

    if not config:
        msg = 'Invalid configuration file'
        click.secho(msg, fg='red', bold=True, err=True)
        click.get_current_context().exit(1)

    # Convert the money.
    converted_amount = convert_money(origin_currency, target_currency, amount)

    # Check if the conversion completed successfully.
    # If not, print and error message and exit the cli.
    if not converted_amount:
        msg = (f'One of the currency codes: {origin_currency} or '
               f'{target_currency} is invalid')
        click.secho(msg, fg='red', bold=True, err=True)
        click.get_current_context().exit(1)

    # Calculate the amount of money to give back to the user
    commission = config.get('base_commission', 5)
    commission_percent = commission / 100
    profit = converted_amount * commission_percent
    amount_after_commission = converted_amount - profit

    # Print summery.
    msg = """
    From Amount: {origin_amount}
    From Currency: {origin_currency}
    To Currency: {target_currency}
    Commission: {commission}%
    Amount Before commission: {converted_amount}
    Amount: {amount}
    """.format(origin_amount=amount,
               origin_currency=origin_currency,
               target_currency=target_currency,
               commission=commission,
               converted_amount=converted_amount,
               amount=amount_after_commission)

    click.secho(msg, fg='green')
