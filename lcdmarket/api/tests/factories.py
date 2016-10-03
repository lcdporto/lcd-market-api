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

