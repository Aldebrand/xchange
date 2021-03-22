from typing import Optional, Tuple

from operations.utils import convert_money, load_config


def exchange(amount: int, origin_currency: str,
             target_currency: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Exchange a certain amount of money from one currency to another.

    :param amount: Amount of money to exchange
    :param origin_currency: Original currency
    :param target_currency: Target currency (defaults to EUR)
    """
    # Load the configuration before exchanging the money in order to exchange.
    # it with the right commission.
    # If something went wrong, return an error message.
    config = load_config()

    if not config:
        error_msg = 'Invalid configuration file'

        return None, error_msg

    # Convert the money.
    converted_amount = convert_money(origin_currency, target_currency, amount)

    # Check if the conversion completed successfully.
    # If not, return an error message.
    if not converted_amount:
        error_msg = (f'One of the currency codes: {origin_currency} or '
                     f'{target_currency} is invalid')

        return None, error_msg

    # Calculate the amount of money to give back to the user.
    commission = config.get('base_commission', 5)
    commission_percent = commission / 100
    profit = converted_amount * commission_percent
    amount_after_commission = converted_amount - profit

    # Build summery message.
    success_msg = """
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

    return success_msg, None
