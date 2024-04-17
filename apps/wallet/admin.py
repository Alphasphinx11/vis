from django.contrib import admin
from .models import walletsettings, Deposit, wallet, Withdrawal

class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet', 'amount', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'amount')
    actions = ['mark_as_approved']

    def mark_as_approved(self, request, queryset):
        for deposit in queryset:
            if request.user.is_superuser:  # Ensure the user is admin
                deposit.status = Deposit.APPROVED
                deposit.save()
                # Update the user's wallet balance
                deposit.wallet.wallet_balance += deposit.amount
                deposit.wallet.save()
    mark_as_approved.short_description = 'Mark selected deposits as Approved'



    def save_model(self, request, obj, form, change):
        if change:  # Check if the deposit is being changed (status updated)
            old_obj = Deposit.objects.get(pk=obj.pk)
            if old_obj.status == Deposit.PENDING and obj.status == Deposit.APPROVED:
                obj.wallet.wallet_balance += obj.amount
                obj.wallet.save()
        super().save_model(request, obj, form, change)

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet', 'amount', 'walletAddress', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'amount')
    actions = ['mark_as_approved']

    def mark_as_approved(self, request, queryset):
        for withdrawal in queryset:
            if request.user.is_superuser:  # Ensure the user is admin
                withdrawal.status = Deposit.APPROVED
                withdrawal.save()
                # Update the user's wallet balance
                withdrawal.wallet.wallet_balance += withdrawal.amount
                withdrawal.wallet.save()
    mark_as_approved.short_description = 'Mark selected withdrawals as Approved'



class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_balance', 'referral_balance', 'trade_balance', 'profit_balance')
    search_fields = ('user__username', 'user__email')

# Register the WalletAdmin with the wallet model
admin.site.register(wallet, WalletAdmin)

# Register the DepositAdmin with the Deposit model
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)



admin.site.register(walletsettings)

