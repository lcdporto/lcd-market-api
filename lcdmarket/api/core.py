"""
Templated Email Definition
"""
import logging

from django.conf import settings

from post_office import mail
from post_office.models import EmailTemplate

from lcdmarket.api import utils

LOGGER = logging.getLogger(__name__)

class TemplatedEmail(object):
    """
    Class responsible for getting and validating the
    email context and preparing the email for sending
    """
    template = None
    context = None
    context_data = {}
    data = None

    def __init__(self):
        self.validate_context()
        assert self.template, 'Must set template attribute on subclass.'

    def validate_context(self):
        """
        Make sure there are no duplicate context objects
        or we might end up with switched data

        Converting the tuple to a set gets rid of the
        eventual duplicate objects, comparing the length
        of the original tuple and set tells us if we
        have duplicates in the tuple or not
        """
        if self.context and len(self.context) != len(set(self.context)):
            LOGGER.error('Cannot have duplicated context objects')
            raise Exception('Cannot have duplicated context objects.')

    def get_instance_of(self, model_cls):
        """
        Search the data to find a instance
        of a model specified in the template
        """
        for obj in self.data.values():
            if isinstance(obj, model_cls):
                return obj
        LOGGER.error('Context Not Found')
        raise Exception('Context Not Found')

    def get_context(self):
        """
        Create a dict with the context data
        """
        assert isinstance(self.context, tuple), 'Expected a Tuple not {0}'.format(type(self.context))
        if not self.context:
            return
        for model in self.context:
            model_cls = utils.get_model_class(model)
            key = utils.camel_to_snake(model_cls.__name__)
            self.context_data[key] = self.get_instance_of(model_cls)

    def get_extra_context(self):
        """
        Override this method if you want to provide
        extra context. The extra_context must be a dict.
        Be very careful no validation is being performed.
        """
        return {}

    def send(self, to, **data):
        """
        This is the method to be called
        """
        self.data = data
        self.get_context()
        # merge the dicts context_data and extra_context
        self.context_data.update(self.get_extra_context())
        if settings.EMAIL_SEND_EMAILS:
            try:
                mail.send(to, template=self.template, context=self.context_data)
            except EmailTemplate.DoesNotExist:
                msg = 'Trying to use a non existent email template {0}'.format(self.template)
                LOGGER.error('Trying to use a non existent email template {0}'.format(self.template))
