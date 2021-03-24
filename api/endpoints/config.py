from django.urls import path
from pydantic import ValidationError as PydanticValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.validations.requests import ConfigRequest
from operations import config as ops_config


@api_view(['PATCH'])
def update_commission(request: Request) -> Response:

    # Validating the request data
    try:
        print('hi')
        new_commission = float(request.data.get('commission'))
        ConfigRequest(commission=new_commission)
    except ValueError:
        return Response('commission must be of type int or float',
                        status.HTTP_400_BAD_REQUEST)
    except PydanticValidationError as pve:
        return Response(pve.json(), status.HTTP_400_BAD_REQUEST)

    config = ops_config.load_config()
    config['base_commission'] = new_commission
    ops_config.update_config(config)

    try:
        ops_config.update_config(config)
    except Exception:
        # We don't want to expose the original reason of the failure
        # since it might contain sensitive information.
        msg = 'Somethign went wrong while trying to update the base commission'

        return Response(msg, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status.HTTP_204_NO_CONTENT)


URLS = [path('config/commission', update_commission, name='update_commission')]
