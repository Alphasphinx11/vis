from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.contrib.auth.decorators import login_required
from django.conf import settings


class walletsettings(models.Model):
    btc_deposit_wallet = models.CharField(max_length= 150, default= "8e00r18393111182840847fihkjle")
    usdt_deposit_wallet = models.CharField(max_length= 150, default= "8e00r18393111182840847fihkjle")


class wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    wallet_balance= models.DecimalField(default= 0.0, max_digits= 50, decimal_places= 2)
    referral_balance = models.DecimalField(default = 0.0, max_digits= 50, decimal_places= 2)
    trade_balance = models.DecimalField(default= 0.0, max_digits= 50, decimal_places= 2)
    profit_balance = models.DecimalField(default= 0.0, max_digits= 50, decimal_places= 2)
    referral_link = models.CharField(max_length=10, null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_wallet(sender, instance, created, **kwargs):
        if created:
            # Create a wallet for the newly created user
            wallet.objects.create(user=instance)



class Deposit(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wallet = models.ForeignKey(wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    
    def approve_deposit(self):
        if self.status == self.APPROVED:
            # Retrieve the user associated with the deposit
            user = self.user
            
            # Check if the user has a wallet
            if user and hasattr(user, 'wallet'):
                user_wallet = user.wallet
                user_wallet.wallet_balance += self.amount
                user_wallet.save()
                
                # Reset status to pending after updating balance
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

class Withdrawal(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    wallet= models.ForeignKey(wallet, on_delete= models.CASCADE)
    amount = models.CharField(max_length=50)
    walletAddress=models.CharField(max_length=200, null= True, blank =True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def verify_transaction(self):
        # Placeholder for verification logic
        self.status = self.APPROVED
        self.save()

        if self.status == self.APPROVED:
            # Update wallet balance upon approval
            self.wallet.wallet_balance += float(self.amount)
            self.wallet.save()

    

    # def generate_referral_link(self):
    #     website_name = "your_website_name"  # Replace with your actual website name
    #     uuid_suffix = str(uuid.uuid4())[:8]  # Use the first 8 characters of the UUID
    #     return f"http://{website_name}/signup?ref={self.referral_code}-{uuid_suffix}"
    
    # def save(self, *args, **kwargs):
    #     if not self.referral_code:
    #         self.referral_code = "100595856" 
    #     super().save(*args, **kwargs)