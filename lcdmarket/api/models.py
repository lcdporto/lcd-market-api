from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.db.models import Max, Sum, F, ExpressionWrapper
#from django.core.validators import MinLengthValidator, RegexValidator
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

from lcdmarket.api.exceptions import InsuficientFunds

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
    is_system = models.BooleanField(default=False)
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
    """
    Products with null quantity means unlimited
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    value = models.IntegerField(null=False)
    is_approved = models.BooleanField(default=False)
    quantity = models.PositiveSmallIntegerField(null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Transfer(models.Model):
    name = models.CharField(max_length=50)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    product = models.ForeignKey('Product', null=True)
    account = models.ForeignKey('Account', related_name='origin')
    target_account = models.ForeignKey('Account', related_name='target', null=True)
    is_pendent = models.BooleanField(default=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'transfer ' + str(self.id)

    def check_balance(self):
        """
        Check if origin account has suficient funds
        """
        if self.amount > self.account.balance:
            raise InsuficientFunds

    def request_transfer(self):
        """
        For now product transactions are
        requests for a transfer
        """
        if not self.pk:
            self.target_account = self.account
            self.account = Account.objects.get(is_system=True)
            self.amount = self.product.value
            self.description = self.product.name

    def set_transfer_description(self):
        """
        Returns transfer description or default
        """
        if not self.description:
            message = 'transfer from {0} to {1}'
            self.description = message.format(
                self.account.full_name, self.target_account.full_name)

    def save(self, *args, **kwargs):
        # check if this is a product transaction
        # or a simple value transfer
        if not self.product:
            self.check_balance()
            self.is_pendent=False
            self.set_transfer_description()
        else:
            # for now we assume only system is seller
            self.request_transfer()
        super(Transfer, self).save(*args, **kwargs)

def aggregate(manager):
    """
    Return related manager sum aggregate
    """
    return manager.exclude(is_pendent=True).aggregate(
        Sum(F('amount')))['amount__sum'] or 0

def get_balance(account):
    """
    Return account balance
    """
    return aggregate(account.target) - aggregate(account.origin)

@receiver(post_save, sender=Transfer)
def update_balance(instance, sender, **kwargs):
    """
    Update origin and destination accounts
    """
    for account in [instance.account, instance.target_account]:
        account.balance = get_balance(account)
        account.save()

@receiver(post_save, sender=Transfer)
def update_product_quantity(instance, sender, **kwargs):
    """
    Update product quantity
    """
    if instance.product and not instance.is_pendent:
        print('a product transaction just happend')
        instance.product.quantity -= 1
        instance.product.save()
