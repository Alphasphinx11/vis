from django.contrib import admin
from .models import Trade

class TradeAdmin(admin.ModelAdmin):
    list_display = ['user', 'symbol', 'amount', 'profit', 'type', 'lot_size', 'duration', 'status']
    list_editable = ['amount', 'profit', 'type', 'lot_size', 'duration', 'status']
    def close_selected_trades(self, request, queryset):
        
        for trade in queryset:
            if trade.status == 'open':
                # Calculate profit
                profit = Decimal(trade.profit) 

                # Update wallet balance with profit
                trade.user.wallet.trade_balance += profit
                trade.user.wallet.save()
                
                # Set status to closed
                trade.status = 'closed'
                trade.save()
        
        self.message_user(request, f"{len(queryset)} trades successfully closed. Total profit: {profit}.")

    close_selected_trades.short_description = "Close selected trades"

admin.site.register(Trade, TradeAdmin)

# Register your models here.
