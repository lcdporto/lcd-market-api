from django.contrib import admin

from lcdmarket.api import models

class AccountAdmin(admin.ModelAdmin):
    """
    Account Admin
    """
    list_display = ('first_name', 'last_name', 'email', 'balance', 'is_active', 'is_staff', 'is_superuser', 'is_system')
    list_filter = ('balance', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')

class ProductAdmin(admin.ModelAdmin):
    """
    Product Admin
    """
    list_display = ('name', 'value', 'quantity', 'is_approved')
    list_filter = ('value', 'quantity')
    search_fields = ('name', 'description')

class TransferAdmin(admin.ModelAdmin):
    """
    Transfer Admin
    """
    list_display = ('transfer', 'name', 'account', 'target_account', 'amount', 'is_pendent')
    list_filter = ('amount', 'is_pendent')

    def transfer(self, obj):
        return 'Transfer {0}'.format(obj.pk)

admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Transfer, TransferAdmin)
