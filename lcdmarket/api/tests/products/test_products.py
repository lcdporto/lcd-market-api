"""
Testing Products
"""

import logging

from lcdmarket.api.tests.testcases import MarketAPITestCase
from lcdmarket.api.tests.factories import ProductFactory


# change default factory boy logging level
logging.getLogger("factory").setLevel(logging.WARN)

class ProductsApi(MarketAPITestCase):
    """
    Testing Products
    """
    def test_guest_can_retrieve_products(self):
        """
        Ensures guest can retrieve products
        """
        product = ProductFactory(value = 5, is_approved=True)

        response = self.client.get('/products/')
        self.assert200(response)

        response = self.client.get('/products/{0}/'.format(product.pk))
        self.assert200(response)
