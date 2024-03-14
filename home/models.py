from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class FileInfo(models.Model):
    path = models.URLField()
    info = models.CharField(max_length=255)

    def __str__(self):
        return self.path
    
SYMBOL_CHOICES = [
        ('audusd', 'AUDUSD'),
        ('btcusd', 'BTCUSD'),
        ('ethusd', 'ETHUSD'),
        ('euraud', 'EURAUD'),
        ('eurgbp', 'EURGBP'),
        ('gbpusd', 'GBPUSD'),
        ('jpyusd', 'JPYUSD'),
        ('nzdusd', 'NZDUSD'),
        ('xauusd', 'XAUUSD'),
    ]
TYPE_CHOICES = [
    ('buy', 'BUY'),
    ('sell', 'SELL'),
]
STATUS_CHOICES = [
    ('open', 'OPEN'),
    ('closed', 'CLOSED'),
]   
DURATION_CHOICES = [
    ('30 minutes', '30 MINUTES'),
    ('40 minutes', '40 MINUTES'),
    ('1 hour', '1 HOUR'),
    ('4 hours', '4 HOURS'),
    ('8 hours', '8 HOURS'),
    ('16 hours', '16 HOURS'),
    ('1 day', '1 DAY'),

]  

class Trade(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol= models.CharField(max_length = 15, choices= SYMBOL_CHOICES, default = 'xauusd')
    amount = models.CharField(max_length = 15)
    profit = models.CharField(max_length = 15, blank=True)
    type = models.CharField(max_length =7, choices= TYPE_CHOICES, default= "buy")
    lot_size  = models.CharField(max_length = 15)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    status = models.CharField(max_length=10, choices= STATUS_CHOICES, default= "open")




    

    