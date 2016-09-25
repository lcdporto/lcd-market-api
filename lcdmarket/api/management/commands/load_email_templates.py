import inspect

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_module

from post_office import models

from lcdmarket.api import utils
from lcdmarket.api.core import TemplatedEmail


class Command(BaseCommand):

    def handle(self, *args, **options):
        templates = self.get_apps()
        self.create_templates(templates)

    def get_apps(self):
        """
        Get the list of installed apps
        and return the apps that have
        an emails module
        """
        templates = []
        for app in settings.INSTALLED_APPS:
            try:
                app = import_module(app + '.emails')
                templates += self.get_solomail_subs(app)
            except ImportError:
                pass
        return templates

    def get_solomail_subs(self, app):
        """
        Returns a list of tuples, but it should
        return a list of dicts
        """
        classes = []
        members = inspect.getmembers(app)
        for member in members:
            name, cls = member
            if inspect.isclass(cls) and issubclass(cls, TemplatedEmail) and name != 'TemplatedEmail':
                try:
                    subject = cls.subject
                    description = cls.description
                    location = app.__file__
                    classes.append((name, location, subject, description))
                except AttributeError:
                    raise AttributeError('Email class must specify email subject and description.')
        return classes

    def create_templates(self, templates):
        """
        Gets a list of templates to insert into the database
        """
        for template in templates:
            name, location, subject, description = template
            if not self.template_exists_db(name):
                # create template if it does not exists
                # if does not exist, try to find a default template
                dir_ = location[:-9] + 'templates/emails/'
                file_ = dir_ + utils.camel_to_snake(name) + '.html'
                text = self.open_file(file_)
                data = {
                    'name': utils.camel_to_snake(name).upper(),
                    'html_content': text,
                    'content': self.text_version(text),
                    'subject': subject,
                    'description': description
                }
                models.EmailTemplate.objects.create(**data)

    def text_version(self, html):
        """
        Uses util to create a text email template
        from a html one
        """
        return utils.html_to_text(html)

    def open_file(self, file_):
        """
        Receives a file path has input and returns a
        string with the contents of the file
        """
        with open(file_, 'r', encoding='utf-8') as file:
            text = ''
            for line in file:
                text += line
        return text

    def template_exists_db(self, template):
        """
        Receives a template name and sees if it exists in the database
        """
        template = utils.camel_to_snake(template).upper()
        try:
            models.EmailTemplate.objects.get(name=template)
        except models.EmailTemplate.DoesNotExist:
            return False
        return True
