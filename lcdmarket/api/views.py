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
from lcdmarket.api import permissions as custom_permissions
from lcdmarket.api import utils
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route

class AccountViewSet(viewsets.ModelViewSet):
    """
    Account View Set
    """
    serializer_class = serializers.AccountSerializer
    search_fields = ('first_name', 'last_name', 'email')
    permission_classes = [custom_permissions.AccountCustomPermission]
    ordering_fields = ('id', )
    ordering = 'id'

    @list_route()
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = models.Account.objects.all()
        if self.request.user.is_authenticated() and self.request.user.is_admin:
            return queryset
        return queryset.filter(is_public=True)

class ProductViewSet(viewsets.ModelViewSet):
    """
    Product View Set
    """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    
class TransferViewSet(viewsets.ModelViewSet):
    """
    Transfer View Set
    """
    queryset = models.Transfer.objects.all()
    serializer_class = serializers.TransferSerializer
    permission_classes = [permissions.IsAuthenticated]
