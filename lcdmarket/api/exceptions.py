from django.utils.translation import ugettext as _

from rest_framework.exceptions import APIException
from rest_framework import status

class InsuficientFunds(APIException):
    """
    Raised when transfer amount is superior to account balance
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Insuficient Funds.')
