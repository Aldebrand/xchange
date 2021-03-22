from pydantic import BaseModel, PositiveFloat
from pydantic.types import constr

CURRENCY_REGEX = r'[a-zA-Z]{3}'


class ExchangeRequest(BaseModel):
    """
    Validates the data of an exchange request.
    """
    amount: PositiveFloat
    origin_currency: constr(regex=CURRENCY_REGEX)
    target_currency: constr(regex=CURRENCY_REGEX)


class ConfigRequest(BaseModel):
    """
    Validates the data of a config commission request.
    """
    commission: PositiveFloat


class LoanRequest(BaseModel):
    """
    Validates the data of a loan request.
    """
    commission: PositiveFloat


class EndLoanRequest(BaseModel):
    """
    Validates the data of an end loan request.
    """
    loan_id: PositiveFloat
    target_currency: constr(regex=CURRENCY_REGEX)
