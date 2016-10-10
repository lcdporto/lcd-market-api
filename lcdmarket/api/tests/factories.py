"""
Factory Boy Factory Definition
"""

from factory.django import DjangoModelFactory as Factory
from factory import LazyAttribute, Sequence, SubFactory

from lcdmarket.api import models

class ProductFactory(Factory):
    """
    Product Factory
    """
    name = Sequence(lambda n: 'Product {0}'.format(n))

    # pylint: disable=R0903
    class Meta:
        """
        Metaclass Definition
        """
        model = models.Product

class AccountFactory(Factory):
    """
    Account Factory
    """
    email = LazyAttribute(lambda m: '{0}@example.com'.format(m.first_name))
    first_name = Sequence(lambda n: 'User{0}'.format(n))
    last_name = 'Smith'

    # pylint: disable=R0903
    class Meta:
        """
        Metaclass Definition
        """
        model = models.Account

class SystemFactory(AccountFactory):
    """
    System Factory
    """
    is_staff = True
    is_system = True
    is_superuser = True
    balance = 50000

class TransferFactory(Factory):
    """
    Transfer Factory
    """

    name = Sequence(lambda n: 'Transfer{0}'.format(n))
    account = SubFactory(AccountFactory)

    class Meta:
        """
        Metaclass Definition
        """
        model = models.Transfer
