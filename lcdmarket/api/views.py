"""
Api View Sets
"""

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from lcdmarket.api import models
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from lcdmarket.api import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route

from lcdmarket.api import utils
from lcdmarket.api import emails

class AccountViewSet(viewsets.ModelViewSet):
    """
    Account View Set
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.AccountSerializer
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'balance')
    ordering = 'id'

    @list_route()
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = models.Account.objects.all()
        if self.request.user.is_authenticated() and self.request.user.is_system:
            return queryset
        return queryset.exclude(is_system=True)

    def get_serializer(self, *args, **kwargs):
        """
        """
        if self.request.user.is_anonymous():
            kwargs['guest_view'] = True
        return super(AccountViewSet, self).get_serializer(*args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    """
    Product View Set
    """
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ('name', 'description')
    filter_fields = ('value', 'is_approved', 'quantity', 'is_fine')

    def perform_create(self, serializer):
        serializer.save()
        if not (self.request.user.is_system and self.is_approved):
            data = {'product': self}
            utils.to_system(emails.ProductSuggested, **data)

    def get_queryset(self):
        queryset = models.Product.objects.all()
        if self.request.user.is_authenticated() and self.request.user.is_system:
            return queryset
        return queryset.filter(is_approved=True).exclude(quantity=0)

    def get_serializer(self, *args, **kwargs):
        """
        Passes extra kwarg to serializer class
        if user is admin, to allow for read_only_fields
        modification on runtime
        """
        if self.request.user.is_authenticated() and self.request.user.is_system:
            kwargs['override_is_approved'] = True
        return super(ProductViewSet, self).get_serializer(*args, **kwargs)
    
class TransferViewSet(viewsets.ModelViewSet):
    """
    Transfer View Set
    """
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = ('is_pendent', 'account', 'target_account', 'product', 'amount')

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

    def get_serializer(self, *args, **kwargs):
        """
        Passes extra kwarg to serializer class
        if user is admin, to allow for read_only_fields
        modification on runtime
        """
        if self.request.user.is_authenticated() and self.request.user.is_system:
            kwargs['override_is_pendent'] = True
        return super(TransferViewSet, self).get_serializer(*args, **kwargs)
