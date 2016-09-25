"""
Email Template Definition
"""

from lcdmarket.api.core import TemplatedEmail

class RequestCreated(TemplatedEmail):
    """
    Email sent to system when a request for transfer is created
    """
    template = 'REQUEST_CREATED'
    context = ('Transfer', )
    description = 'Email sent to system when a transfer request is created'
    subject = 'Pedido de Transferência Recebido.'

class RequestApproved(TemplatedEmail):
    """
    Email sent to user after transfer approval by system
    """
    template = 'REQUEST_APPROVED'
    context = ('Transfer', )
    description = 'Email sent to user when we receive confirmation of a payment'
    subject = 'Transferência efetuada.'
