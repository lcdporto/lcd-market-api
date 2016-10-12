from django.contrib import admin

from lcdmarket.api import models
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponseRedirect
from django.template import RequestContext


class FineForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    product = forms.ModelChoiceField(models.Product.objects.filter(is_fine = True))

class AccountAdmin(admin.ModelAdmin):
    """
    Account Admin
    """
    list_display = ('first_name', 'last_name', 'email', 'balance', 'is_active', 'is_staff', 'is_superuser', 'is_system')
    list_filter = ('balance', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    actions = ['apply_fine']

    def apply_fine(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = FineForm(request.POST)

            if form.is_valid():
                product = form.cleaned_data['product']
                for account in queryset:
                    account.apply_fine(product)
                self.message_user(request, "Fine applied to selected accounts")
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = FineForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        opts = self.model._meta
        app_label = opts.app_label

        context = {'accounts': queryset, 'product_form': form, 'opts': opts, 'app_label': app_label}
        return render_to_response('admin/apply_fine.html', context, RequestContext(request))

class ProductAdmin(admin.ModelAdmin):
    """
    Product Admin
    """
    list_display = ('name', 'value', 'quantity', 'is_approved', 'is_fine', 'is_reward', 'seller')
    list_filter = ('value', 'quantity', 'is_fine', 'is_approved', 'is_reward')
    search_fields = ('name', 'description', 'seller')

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
