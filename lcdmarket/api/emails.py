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

class ProductSuggested(TemplatedEmail):
    """
    Email sent to system when a product is suggested (created by a normal user - is_approved = False)
    """
    template = 'PRODUCT_SUGGESTED'
    context = ('Product', )
    description = 'Email sent to system when a product is suggested'
    subject = 'Sugestão de Produto Recebida.'