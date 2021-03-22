from django.urls import path
from pydantic import ValidationError as PydanticValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.validations.requests import EndLoanRequest, LoanRequest
from operations import loan as ops_loan


@api_view(['POST'])
def loan(request: Request) -> Response:
    amount = request.data.get('amount')
    currency = request.data.get('currency')

    # Validating the request data
    try:
        LoanRequest(amount=amount, currency=currency)
    except PydanticValidationError as pve:
        return Response(pve.json(), status.HTTP_400_BAD_REQUEST)

    loan_id, success_msg, error_msg = ops_loan.loan(amount, currency)

    if error_msg:
        # We don't want to expose the original reason of the failure
        # since it might contain sensitive information.
        msg = 'Cannot create a loan transaction at the moment'

        return Response(msg, status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = {'message': success_msg, 'loan_id': loan_id}

    return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
def end_loan(request: Request) -> Response:
    loan_id = request.query_params.get('loanId')
    target_currency = request.query_params.get('targetCurrency')

    # Validating the request data
    try:
        EndLoanRequest(loan_id=loan_id, target_currency=target_currency)
    except PydanticValidationError as pve:
        return Response(pve.json(), status.HTTP_400_BAD_REQUEST)

    success_msg, error_msg = ops_loan.end_loan(loan_id, target_currency)

    if error_msg:
        # We don't want to expose the original reason of the failure
        # since it might contain sensitive information,
        msg = 'Cannot end the loan at the moment'

        return Response(msg, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(success_msg, status.HTTP_200_OK)


URLS = [
    path('loan', loan, name='loan'),
    path('loan/end', end_loan, name='end_loan')
]
