"""
Testing Transfers
"""

import logging
from lcdmarket.api.tests.testcases import MarketAPITestCase
from lcdmarket.api.tests.factories import TransferFactory, AccountFactory, ProductFactory, SystemFactory

# change default factory boy logging level
logging.getLogger("factory").setLevel(logging.WARN)

class TransfersApi(MarketAPITestCase):
    """
    Testing Transfers
    """
    def test_guest_cannot_transfer_tokens(self):
        """
        Ensures guest cannot transfer tokens to another account
        """
        user = AccountFactory()
        transfer = {
            'amount' : 50,
            'target_account' : user.pk
        }

        response = self.client.post('/transfers/',transfer)
        self.assert403(response)

    def test_guest_cannot_take_a_offer_from_market(self):
        """
        Ensures guest cannot take a offer from market - transfer from system to user
        """
        system = SystemFactory()
        product = ProductFactory(name = 'P_X', value = 50, is_approved = True, seller = system, is_reward = True)
        transfer = {
            'product' : product.pk,
            'account': system.pk
        }

        response = self.client.post('/transfers/', transfer)
        self.assert403(response)

    def test_user_can_take_a_offer_from_market(self):
        """
        Ensures user can take a offer from market
        """
        system = SystemFactory()
        product = ProductFactory(name='P_X', value=50, is_approved=True, seller=system, is_reward = True)
        user = AccountFactory(balance = 100)
        self.client.force_authenticate(user)
        transfer = {
            'product': product.pk,
            'account': user.pk
        }

        response = self.client.post('/transfers/', transfer)
        self.assert201(response)
        self.assertFieldEqual(response, 'amount', product.value)
        self.assertFieldEqual(response, 'target_account', user.pk)

    def test_user_cannot_exceed_balance(self):
        """
        Ensures user cannot exceed its balance
        """
        user1 = AccountFactory(balance = 50)
        self.client.force_authenticate(user1)
        user2 = AccountFactory()
        transfer = {
            'amount': 60,
            'account': user1.pk,
            'target_account' : user2.pk
        }

        response = self.client.post('/transfers/', transfer)
        self.assert400(response)

    def test_user_can_buy_something_from_system(self):
        """
        Ensures user can buy something from system
        """
        system = SystemFactory()
        product = ProductFactory(name='P_X', value=50, is_approved=True, seller=system)
        user = AccountFactory(balance=100)
        self.client.force_authenticate(user)
        transfer = {
            'product': product.pk,
            'account': user.pk
        }

        response = self.client.post('/transfers/', transfer)
        self.assert201(response)
        self.assertFieldEqual(response, 'amount', product.value)
        self.assertFieldEqual(response, 'target_account', system.pk)

    def test_user_can_buy_something_from_other_user(self):
        """
        Ensures user can buy something from other user
        """
        seller = AccountFactory(is_staff=True, balance=500)
        product = ProductFactory(name='P_S', value=50, is_approved=True, seller=seller)
        user = AccountFactory(balance=100)
        self.client.force_authenticate(user)
        transfer = {
            'product': product.pk,
            'account': user.pk
        }

        response = self.client.post('/transfers/', transfer)
        self.assert201(response)
        self.assertFieldEqual(response, 'amount', product.value)
        self.assertFieldEqual(response, 'target_account', seller.pk)
