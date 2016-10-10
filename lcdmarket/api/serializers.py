"""
Custom serializer classes for api application
"""

from rest_framework import serializers
from lcdmarket.api import models

class AccountSerializer(serializers.ModelSerializer):
    """
    account serializer class
    """
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        """
        Overrides init to provide a simpler serialization
        """
        guest_view = kwargs.pop('guest_view', None)
        super(AccountSerializer, self).__init__(*args, **kwargs)
        if guest_view:
            for f in ['email', 'is_superuser', 'is_active', 'is_staff']:
                self.fields.pop(f)

    def create(self, validated_data):
        return models.Account.objects.create_user(**validated_data)

    class Meta:
        model = models.Account
        fields = ('id', 'avatar',  'email', 'first_name', 'last_name', 'full_name', 'balance',  'is_superuser', 'password',
                  'is_staff', 'is_active', 'created', 'updated', )
        read_only_fields = ('is_staff', 'is_active', 'is_superuser', 'balance', 'created', 'updated', 'balance')


class ProductSerializer(serializers.ModelSerializer):
    """
    Product Serializer
    """

    def __init__(self, *args, **kwargs):
        """
        Overrides init to provide a mechanism to change
        read_only_fields on runtime
        """
        override_is_approved = kwargs.pop('override_is_approved', None)
        super(ProductSerializer, self).__init__(*args, **kwargs)
        if override_is_approved:
            self.fields['is_approved'].read_only = False

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'description', 'value', 'is_approved', 'quantity', 'is_fine', 'is_reward', 'seller')
        read_only_fields = ('is_approved', 'seller')

class TransferSerializer(serializers.ModelSerializer):
    """
    Transfer Serializer
    """
    amount = serializers.IntegerField(min_value=1, required=False)
    product = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        queryset=models.Product.objects.filter(is_approved=True).exclude(quantity=0),
        required=False
    )

    def __init__(self, *args, **kwargs):
        """
        Overrides init to provide a mechanism to change
        read_only_fields on runtime
        """
        override_is_pendent = kwargs.pop('override_is_pendent', None)
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if override_is_pendent:
            self.fields['is_pendent'].read_only = False

    class Meta:
        model = models.Transfer
        fields = ('id', 'amount', 'product', 'account', 'target_account', 'is_pendent', 'description', 'created', 'updated')
        read_only_fields = ('account', 'is_pendent')
