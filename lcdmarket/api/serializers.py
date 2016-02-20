"""
Custom serializer classes for api application
"""

from rest_framework import serializers
from lcdmarket.api import models

class AccountSerializer(serializers.ModelSerializer):
    """
    account serializer class
    """
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = models.Account
        fields = ('id', 'avatar',  'email', 'first_name', 'last_name', 'full_name', 'balance',  'is_superuser', 'password', 'confirm_password',
                  'is_staff', 'is_active', 'is_public',  'created', 'updated', )
        read_only_fields = ('is_staff', 'is_active', 'is_superuser', 'balance', 'created', 'updated', 'balance')


class ProductSerializer(serializers.ModelSerializer):
    """
    Product Serializer
    """
    class Meta:
        model = models.Product
        fields = ('id', 'name', 'description', 'value')

class TransferSerializer(serializers.ModelSerializer):
    """
    Transfer Serializer
    """
    class Meta:
        model = models.Transfer
        fields = ('id', 'amount', 'product', 'account', 'target_account', 'is_pendent')
        read_only_fields = ('amount', 'is_pendent')
