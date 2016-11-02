"""
Utils
"""
import logging
import re
from lxml import html
import requests
# TODO: this does not make sense we should be using
# requests instead of urllib
from urllib import request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.apps import apps

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

LOGGER = logging.getLogger(__name__)


def to_email(email_class, email, **data):
    """
    Send email to specified email address
    """
    email_class().send([email], **data)


def to_user(email_class, user, **data):
    """
    Send email to a registered user
    """
    email_class().send([user.email], **data)


def to_system(email_class, **data):
    """
    Send email to system user
    """
    for user in get_user_model().objects.filter(is_system=True):
        email_class().send([user.email], **data)


def get_model_class(name):
    """
    This is being implemented to help
    with the Email feature

    Beware that currently implementation
    returns the first match, so if a model
    with a same name exists in two different
    applications this will not work

    http://stackoverflow.com/a/13242421
    """
    LOGGER.warning('Beware, function returns first match in the model registry.')
    # iterate all registered models
    for model in apps.get_models():
        # return the app_label for first match
        if name == model._meta.object_name:
            app_label = model._meta.app_label
    return apps.get_model(app_label, name)


def camel_to_snake(name):
    """
    Convert from CamelCase to snake_case
    http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(word, lower_first=True):
    """
    Convert from snake_case to CamelCase
    """
    result = ''.join(char.capitalize() for char in word.split('_'))
    if lower_first:
        return result[0].lower() + result[1:]
    else:
        return result


def html_to_text(html_string):
    """
    returns a plain text string when given a html string text
    handles a, p, h1 to h6 and br, inserts newline chars to
    create space in the string
    """

    # create a valid html document from string
    # beware that it inserts <hmtl> <body> and <p> tags
    # where needed
    html_tree = html.document_fromstring(html_string)

    # handle header tags
    for h in html_tree.cssselect("h1, h2, h3, h4, h5, h6"):
        # add two newlines after a header tag
        h.text = h.text + '\n\n'

    # handle links
    # find all a tags starting from the root of the document //
    # and replace the link with (link)
    for a in html_tree.xpath("//a"):
        href = a.attrib['href']
        a.text = a.text + " (" + href + ")"

    # handle paragraphs
    for p in html_tree.xpath("//p"):
        # keep the tail if there is one
        # or add two newlines after the text if there is no tail
        p.tail = p.tail if p.tail else "\n\n"

    # handle breaks
    for br in html_tree.xpath("//br"):
        # add a newline and then the tail (remaining text after the <br/> tag)
        # or add a newline only if there is no tail
        # http://stackoverflow.com/a/18661076
        br.tail = "\n" + br.tail if br.tail else "\n"

    return html_tree.text_content()


def get_fields(dic, fields):
    """
    Create a dict from an old dict using a list
    of fields, if the field does not exist this is going
    to blow up
    """
    return { k: dic[k] for k in fields }


def get_remote_user_data(token):
    """
    Get remote user data from auth server
    """
    token = str(token, 'utf-8')
    headers = {"Authorization":"Bearer {0}".format(token)}
    try:
        return requests.get(settings.AUTH_SERVER + 'users/me/', headers=headers).json()
    except requests.exceptions.ConnectionError:
        msg = _('Remote API not available, please try again later.')
        raise exceptions.AuthenticationFailed(msg)


def get_remote_avatar(avatar):
    """
    Get remote user avatar
    """
    url = settings.AUTH_SERVER + 'static/media/' + avatar
    tmp = NamedTemporaryFile(delete=True)
    tmp.write(request.urlopen(url).read())
    tmp.flush()
    return File(tmp)


def create_local_user(token):
    """
    Create local user
    """
    # retrieve data
    data = get_remote_user_data(token)
    new_user_data = get_fields(data, ['email', 'first_name', 'last_name', 'avatar'])
    # this is a hack inside a hack, and should be temp
    new_user_data['avatar'] = get_remote_avatar(new_user_data['avatar'])
    # create user
    User = get_user_model()
    new_user = User.objects.create(**new_user_data)
    # make sure user password is unusable
    new_user.set_unusable_password()
    new_user.save()
    return new_user
