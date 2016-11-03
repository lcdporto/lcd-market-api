from django.contrib import admin

from lcdmarket.api import models
from django.shortcuts import render_to_response
from django import forms
from django.http import HttpResponseRedirect
from django.template import RequestContext


class FineForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    product = forms.ModelChoiceField(models.Product.objects.filter(is_fine = True))


class SellerForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    seller = forms.ModelChoiceField(models.Account.objects.all())


class AccountAdmin(admin.ModelAdmin):
    """
    Account Admin
    """
    list_display = ('first_name', 'last_name', 'email', 'balance', 'is_active', 'is_staff', 'is_superuser', 'is_system')
    list_filter = ('balance', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    actions = ['apply_fine']
    icon = '<i class="material-icons">account_circle</i>'

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
    search_fields = ('name', 'description', 'seller__email', 'seller__first_name', 'seller__last_name')
    actions = ['make_reward', 'make_fine', 'change_seller']
    icon = '<i class="material-icons">store</i>'

    def change_seller(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = SellerForm(request.POST)

            if form.is_valid():
                seller = form.cleaned_data['seller']
                rows = queryset.update(seller=seller)
                self.message_user(request, "Seller Updated on {0} products".format(rows))
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = SellerForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        opts = self.model._meta
        app_label = opts.app_label

        context = {'products': queryset, 'seller_form': form, 'opts': opts, 'app_label': app_label}
        return render_to_response('admin/change_seller.html', context, RequestContext(request))


    def make_reward(self, request, queryset):
        """
        Set products as rewards
        """
        # a product cannot be a reward and a fine at the same time
        rows = queryset.update(is_reward=True, is_fine=False)
        self.message_user(request, "The selected products were marked as rewards, total products changed {0}.".format(rows))

    def make_fine(self, request, queryset):
        """
        Set products as fines
        """
        # a product cannot be a reward and a fine at the same time
        rows = queryset.update(is_reward=False, is_fine=True)
        self.message_user(request, "The selected products were marked as fines, total products changed {0}.".format(rows))


class TransferAdmin(admin.ModelAdmin):
    """
    Transfer Admin
    """
    list_display = ('transfer', 'name', 'account', 'target_account', 'amount', 'is_pendent')
    list_filter = ('amount', 'is_pendent')
    actions = ['approve_transfer']
    icon = '<i class="material-icons">swap_horiz</i>'

    def transfer(self, obj):
        return 'Transfer {0}'.format(obj.pk)

    def approve_transfer(self, request, queryset):
        """
        Bulk action to approve pendent transfers
        """
        # we cannot use update here
        for transfer in queryset:
            transfer.is_pendent=False
            transfer.save()
        self.message_user(request, "The selected transfers have been approved.")

admin.site.register(models.Account, AccountAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Transfer, TransferAdmin)
