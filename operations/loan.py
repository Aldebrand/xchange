from datetime import datetime
from typing import Optional, Tuple

import click
from bson.objectid import ObjectId

from operations.utils import convert_money, init_mongo_client, load_config

DATE_FORMAT = '%d/%m/%Y'


def loan(amount: float, currency: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Register a new loan.

    :param amount: Amount of money that the user loaned
    :param currency: Loan currency
    """
    # Load the commissions for loans.
    config = load_config()
    base_commission = config.get('base_commission', 5)
    daily_commission = config.get('daily_commission', 0.5)

    # Initialize a db client and insert the data.
    try:
        client = init_mongo_client()
        db = client['xchange']
        loans_coll = db.get_collection('loans')
        start_date = datetime.today().date().strftime(DATE_FORMAT)
        data = {
            'amount': amount,
            'currency': currency.upper(),
            'start_date': start_date,
            'base_commission': base_commission,
            'daily_commission': daily_commission
        }
        result = loans_coll.insert_one(data)
        client.close()
    except Exception as e:
        error_msg = ('An Unknown error has been occurred while trying to '
                     f'register a new loan: {e}')

        return None, error_msg

    # Build the loan summery message.
    loan_id = str(result.inserted_id)
    success_msg = """Loan Details:
    \tLoan Amount: {loan_amount}
    \tLoan Currency: {loan_currency}
    \tBase Commission: {base_commission}%
    \tDaily Commission: {daily_commission}%
    \tLoan start: {start_date}
    \tLoan id: {id}
    """.format(loan_amount=amount,
               loan_currency=currency.upper(),
               base_commission=base_commission,
               daily_commission=daily_commission,
               start_date=start_date,
               id=loan_id)

    return success_msg, None


def end_loan(loan_id: str,
             target_currency: str) -> Tuple[Optional[str], Optional[str]]:
    """
    End a loan.

    :param loan_id: ID of the loan as it appears in the db
    :param target_currency: Currency to pay the loan
    """
    # Retrieve the loan from the db.
    try:
        client = init_mongo_client()
        db = client['xchange']
        loans_coll = db.get_collection('loans')
        query = {'_id': ObjectId(loan_id)}
        result = loans_coll.find_one(query)
        client.close()
    except Exception as e:
        error_msg = ('An Unknown error has been occurred while trying to '
                     f'retrieve the requested loan: {e}')

        return None, error_msg

    # Extract the data from the result.
    amount = result['amount']
    currency = result['currency']
    start_date_str = result['start_date']
    start_date = datetime.strptime(start_date_str, DATE_FORMAT)
    loan_base_commission = result['base_commission']
    loan_daily_commission = result['daily_commission']

    # Calculate the loan period.
    end_date = datetime.today()
    end_date_str = end_date.date().strftime(DATE_FORMAT)
    delta = end_date - start_date
    days_passed = delta.days

    # Calculate the total commission.
    total_daily_commission = days_passed * loan_daily_commission
    total_commission = total_daily_commission + loan_base_commission
    commission_percent = total_commission / 100

    # Calculate the amount to pay.
    converted_amount = convert_money(currency, target_currency, amount)

    if not converted_amount:
        msg = (f'One of the currency codes: {currency} or '
               f'{target_currency} is invalid')
        click.secho(msg, fg='red', bold=True, err=True)
        click.get_current_context().exit(1)

    profit = converted_amount * commission_percent
    amount_after_commission = round(converted_amount + profit, 3)

    # Build the loan summery message.
    success_msg = """Loan end:
    \tPaid Currency: {paid_currency}
    \tTotal Commission: {total_commission}
    \tLoan Currency: {loan_currency}
    \tPaid Amount Before Commission: {amount_before_commission}
    \tPaid Amount: {amount}
    \tLoan end: {end_date}\nLoan Details:
    \tLoan Amount: {loan_amount}
    \tLoan Currency: {loan_currency}
    \tBase Commission: {base_commission}%
    \tDaily Commission: {daily_commission}%
    \tLoan start: {start_date}
    \tLoan id: {id}
    """.format(loan_amount=amount,
               loan_currency=currency.upper(),
               base_commission=loan_base_commission,
               daily_commission=loan_daily_commission,
               start_date=start_date,
               id=loan_id,
               paid_currency=target_currency.upper(),
               amount_before_commission=converted_amount,
               amount=amount_after_commission,
               end_date=end_date_str,
               total_commission=total_commission)

    return success_msg, None
