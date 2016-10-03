"""
Testing Transfers
"""

import logging
from lcdmarket.api.tests.testcases import MarketAPITestCase
from lcdmarket.api.tests.factories import TransferFactory, AccountFactory, ProductFactory

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
        user = AccountFactory(is_staff = True, is_system = True, is_superuser = True, balance = 50000)
        product = ProductFactory(name = 'P_X', value = 50, is_approved = True)
        transfer = {
            'product' : product.pk,
            'amount' : product.value,
            'account': user.pk
        }

        response = self.client.post('/transfers/', transfer)
        self.assert403(response)

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