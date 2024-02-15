from django.contrib import admin
from .models import Trade

class TradeAdmin(admin.ModelAdmin):
    list_display = ['user', 'symbol', 'amount', 'profit', 'type', 'lot_size', 'duration', 'status']
    list_editable = ['amount', 'profit', 'type', 'lot_size', 'duration', 'status']

admin.site.register(Trade, TradeAdmin)

# Register your models here.
