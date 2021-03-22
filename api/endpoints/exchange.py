from django.urls import path
from pydantic import ValidationError as PydanticValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.validations.requests import ExchangeRequest
from operations import exchange as ops_exchange


@api_view(['GET'])
def exchange(request: Request) -> Response:
    amount = request.query_params.get('amount')
    origin_currency = request.query_params.get('originCurrency')
    target_currency = request.query_params.get('targetCurrency', 'EUR')

    # Validating the request data
    try:
        ExchangeRequest(amount=amount,
                        origin_currency=origin_currency,
                        target_currency=target_currency)
    except PydanticValidationError as pve:
        return Response(pve.json(), status.HTTP_400_BAD_REQUEST)

    success_msg, error_msg = ops_exchange.exchange(amount, origin_currency,
                                                   target_currency)

    if error_msg:
        # We don't want to expose the original reason of the failure
        # since it might contain sensitive information.
        msg = 'Failed to exchange the money'

        return Response(msg, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(success_msg, status.HTTP_200_OK)


URLS = [path('exchange', exchange, name='exchange')]
