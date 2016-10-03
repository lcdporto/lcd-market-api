"""
Custom API Client
"""
from urllib.parse import urlencode
from rest_framework.test import APIClient

class MarketAPIClient(APIClient):
    """
        Subclasses APIClient to provide
        custom functionality
        """

    def parse_params(self, params):
        """
        Parsing params, params is a dict
        and the dict value can be a string
        or an iterable, namely a list, we
        need to process those iterables
        """
        for (key, value) in params.items():
            if not isinstance(value, str):
                string_params = self.to_string(value)
                params[key] = string_params
        return params

    def to_string(self, obj):
        """
        Picks up an object and transforms it
        into a string, by coercing each element
        in an iterable to a string and then joining
        them, or by trying to coerce the object directly
        """
        try:
            converted = [str(element) for element in obj]
            string = ','.join(converted)
        except TypeError:
            # for now this is ok for booleans
            string = str(obj)
        return string

    def filter(self, endpoint, params):
        """
        Makes a get request by construction
        the path from an endpoint and a dict
        with filter query params

        e.g.
        params = {'category__in': [1,2]}
        response = self.client.filter('/experiences/', params)
        """
        params = self.parse_params(params)
        params = urlencode(params)
        path = '{0}?{1}'.format(endpoint, params)
        return self.get(path)