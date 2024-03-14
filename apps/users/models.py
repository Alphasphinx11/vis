from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
import secrets


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = ("email")
    REQUIRED_FIELDS = ["username"]
    
    def _str__(self):
        return self.email


ROLE_CHOICES = (
    ('admin'  , 'Admin'),
    ('user'  , 'User'),
)
class Profile(models.Model):
    user      = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role      = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    country   = models.CharField(max_length=255, null=True, blank=True)
    city      = models.CharField(max_length=255, null=True, blank=True)
    zip_code  = models.CharField(max_length=255, null=True, blank=True)
    address   = models.CharField(max_length=255, null=True, blank=True)
    phone     = models.CharField(max_length=255, null=True, blank=True)
    avatar    = models.ImageField(upload_to='avatar', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
ID_TYPE_CHOICES = [
        ('drivers_license', 'Drivers_License'),
        ('Passport', 'Passport'),
        ('id_card', 'ID_CARD'),
        #('done', 'Done'),
    ]


class Kyc(models.Model):
    user  = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_type = models.CharField(max_length = 50, choices=ID_TYPE_CHOICES, default= "Passport")
    pic    = models.ImageField(upload_to='Kycs', null=True, blank=True)
    selfie = models.ImageField(upload_to='selfies', null=True, blank=True)
    verified = models.BooleanField(default= False)


    def verify_kyc():
        pass

class OtpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    
    def __str__(self):
        return self.user.username
    