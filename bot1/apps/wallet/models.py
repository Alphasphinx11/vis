from django.db import models
from django.contrib.auth.models import User
import uuid

class walletsettings(models.Model):
    default_deposit_wallet = models.CharField(max_length= 150, default= "8e00r18393111182840847fihkjle")


class wallet(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    wallet_balance= models.DecimalField(default= 0.0, max_digits= 50, decimal_places= 6)
    referral_balance = models.DecimalField(default = 0.0, max_digits= 50, decimal_places= 6)
    trade_balance = models.DecimalField(default= 0.0, max_digits= 50, decimal_places= 6)
    profit_balance = models.DecimalField(default= 0.0, max_digits= 50, decimal_places= 6)
    referral_link = models.CharField(max_length= 100)

    def verify_transaction(self):
        # Placeholder for verification logic
        self.deposit_verified = True
        self.save()

    def deposit(self, amount):
        # Placeholder for deposit logic
        if not self.deposit_verified:
            return

        self.wallet_balance += amount
        self.save()

    def withdraw(self, amount):
        # Placeholder for withdrawal logic
        if self.wallet_balance >= amount:
            self.wallet_balance -= amount
            self.save()
        else:
            print("Insufficient funds")

    def open_trade(self, amount):
        # Placeholder for opening a trade logic
        self.trade_balance += amount
        self.save()

    def close_trade(self, amount):
        # Placeholder for closing a trade logic
        if self.trade_balance >= amount:
            self.trade_balance -= amount
            self.profit_balance += amount
            self.save()
        else:
            print("Cannot close trade, insufficient trade balance")
   
    def __str__(self):
        return f"Wallet for {self.user.username}"

    def generate_referral_link(self):
        website_name = "your_website_name"  # Replace with your actual website name
        uuid_suffix = str(uuid.uuid4())[:8]  # Use the first 8 characters of the UUID
        return f"http://{website_name}/signup?ref={self.referral_code}-{uuid_suffix}"
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = "100595856" 
        super().save(*args, **kwargs)