"""
Testing Products
"""

import logging

from lcdmarket.api.tests.testcases import MarketAPITestCase
from lcdmarket.api.tests.factories import ProductFactory, AccountFactory


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

    def test_user_cannot_retrieve_products_not_approved(self):
        """
        Ensures user cannot retrieve products not approved
        """
        user = AccountFactory()
        self.client.force_authenticate(user)

        product = ProductFactory(value=5, is_approved=False)

        response = self.client.get('/products/')
        self.assert200(response)

        response = self.client.get('/products/{0}/'.format(product.pk))
        self.assert404(response)

    def test_user_can_suggest_a_product(self):
        """
        Ensures user can suggest a product
        """
        user = AccountFactory()
        self.client.force_authenticate(user)

        data = {
            'value': 5,
            'name': 'Product'
        }

        response = self.client.post('/products/', data)
        self.assert201(response)
        self.assertFieldEqual(response, 'is_approved', False)

    def test_guest_cannot_add_a_product(self):
        """
        Ensures guest cannot add a product
        """
        data = {
            'value': 10,
            'name': 'GuestProduct'
        }

        response = self.client.post('/products/', data)
        self.assert403(response)

    def test_user_can_add_a_product_to_sell(self):
        """
        Ensures user can add a product to sell
        """
        user = AccountFactory()
        self.client.force_authenticate(user)

        data = {
            'value': 15,
            'name': 'UserProduct',
        }

        response = self.client.post('/products/', data)
        self.assertFieldEqual(response, 'seller', user.pk)