"""
Market API Test Case
"""

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.response import Response

from lcdmarket.api.tests.clients import MarketAPIClient

def check_response_type(response):
    """
    Make sure a response object is an
    instance of REST Framework Response
    """
    assert isinstance(response, Response), 'response must be a rest framework response object'

class MarketAPITestCase(APITestCase):
    """
    Custom APITestCase that provides a APIClient with
    some nice methods and some extra assert methods
    for common use cases
    """

    client_class = MarketAPIClient

    def assertFieldEqual(self, response, field, value):
        """
        Assert that the value of a field is equal to value
        """
        self.assertEqual(response.data.get(field), value)

    def assert200(self, response):
        """
        Assert responses status code is 200
        """
        check_response_type(response)
        self.assertEqual(status.HTTP_200_OK, response.status_code, response.data)

    def assert201(self, response):
        """
        Assert responses status code is 201
        """
        check_response_type(response)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code, response.data)

    def assert204(self, response):
        """
        Assert responses status code is 204
        """
        check_response_type(response)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code, response.data)

    def assert400(self, response):
        """
        Assert responses status code is 400
        """
        check_response_type(response)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)

    def assert403(self, response):
        """
        Assert responses status code is 403
        """
        check_response_type(response)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code, response.data)

    def assert404(self, response):
        """
        Assert responses status code is 404
        """
        check_response_type(response)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code, response.data)

    def assert405(self, response):
        """
        Assert responses status code is 405
        """
        check_response_type(response)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code, response.data)

    def assertResultsLen(self, response, length):
        """
        Assert that the length of a list of results
        is equal to the lenght param

        len(response.data.get('results')) == length
        """
        check_response_type(response)
        assert isinstance(length, int)
        self.assertEqual(len(response.data.get('results')), length)

    def assertRequiredFields(self, response, required_fields, status_code=400):
        """
        Assert response has the status_code response status and the
        message is requiring the fields specified in the
        required_fields dict. By default status code is 400
        """
        check_response_type(response)
        for field in required_fields:
            self.assertContains(response, field, status_code=status_code)

    def assertNonVisibleFields(self, response, fields, status_code=200):
        """
        Assert that fields are not visible in the response.
        By default check that response has status code 200
        """
        check_response_type(response)
        for field in fields:
            self.assertNotContains(response, field, status_code=status_code)

    def assertLogin(self, username, password):
        """
        Assert login, aka, exchange username and password for jwt
        """
        data = {'email': username, 'password': password}
        response = self.client.post('/api-token-auth/', data)
        self.assert200(response)  # to provide debug info
        self.assertContains(response, 'token', status_code=200)

    def assertCannotLogin(self, username, password):
        """
        Assert cannot login, aka, cannot exchange username and password for jwt
        """
        data = {'email': username, 'password': password}
        response = self.client.post('/api-token-auth/', data)
        self.assert400(response)  # to provide debug info
        self.assertNonFieldErrors(response, 'Unable to login with provided credentials.')

    def assertObjFieldEqual(self, obj, field, value):
        """
        Assert field in obj is equal to provided value
        """
        self.assertEqual(getattr(obj, field), value)