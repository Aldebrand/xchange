import click

from operations import loan as ops_loan


@click.command()
@click.argument('amount', type=float, required=True)
@click.argument('currency', type=str, required=True)
def loan(amount: float, currency: str):
    """
    Register a new loan.

    \b
    AMOUNT - amount of money that the user loaned
    CURRENCY - loan currency
    """
    result = ops_loan.loan(amount, currency)
    success_msg = result[1]
    error_msg = result[2]

    if error_msg:
        click.secho(error_msg, fg='red', bold=True, err=True)
        click.get_current_context().exit(1)

    click.secho(success_msg, fg='green')


@click.command(name='end-loan')
@click.argument('loan-id', type=str, required=True)
@click.argument('target-currency', type=str, required=True)
def end_loan(loan_id: str, target_currency: str):
    """
    End a loan.

    \b
    LOAN_ID - ID of the loan as it appears in the db
    TARGET_CURRENCY - currency to pay the loan
    """
    success_msg, error_msg = ops_loan.end_loan(loan_id, target_currency)

    if error_msg:
        click.secho(error_msg, fg='red', bold=True, err=True)
        click.get_current_context().exit(1)

    click.secho(success_msg, fg='green')
