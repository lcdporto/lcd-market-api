from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.db.models import Max
from django.core.validators import MinLengthValidator, RegexValidator

class AccountManager(BaseUserManager):
    """
    Custom Account Model Manager
    """
    
    def create_user(self, email, password=None, **kwargs):
        
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model(
            email=self.normalize_email(email),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name')
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_superuser = True
        account.save()
        return account

# here we are extending the default user model
class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=False, default="default_avatar_200x200.png")
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    balance = models.IntegerField(default=0)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = AccountManager()

    @property
    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    # we will use the email as the username credential
    # the required field here is need because it's the way
    # django wants it when extending the default model (?)
    USERNAME_FIELD = 'email'
    # these fields are used by the createsuperuser command
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        """
        Account string representation in python3
        """
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return None

    def has_perm(self, perm, obj=None):
        return self.is_admin()
    
    def has_module_perms(self, app_label):
        return self.is_admin()

    # we want is_admin to te used as a model property and
    # not has a model method
    # so he have set a @property, for an explanation and example see
    # https://www.stavros.io/posts/how-replace-django-model-field-property/
    @property
    def is_admin(self):
        # admin is a user that satisfies all the following conditions
        # is active, superuser and staff
        return self.is_superuser and self.is_staff and self.is_active


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    value = models.IntegerField(null=False)
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Transfer(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    product = models.ForeignKey('Product')
    account = models.ForeignKey('Account', related_name='origin')
    target_account = models.ForeignKey('Account', related_name='target')
    is_pendent = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'transfer ' + str(self.id)

    def save(self, *args, **kwargs):
        self.amount = self.product.value
        # update account balance
        self.account.balance = self.account.balance + self.product.value
        self.account.save()
        # update target account balance
        self.target_account.balance = self.target_account.balance - self.product.value
        self.target_account.save()
        super(Transfer, self).save(*args, **kwargs)
    
