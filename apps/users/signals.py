from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OtpToken, Profile
from apps.wallet.models import wallet
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.html import strip_tags
from django.template.loader import render_to_string

 
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL) 
def create_token(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        # Create a wallet for the newly created user
        wallet.objects.create(user=instance)
        if instance.is_superuser:
            pass
        
        else:
            OtpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            instance.is_active=False 
            instance.save()
        
        
        # email credentials
            otp = OtpToken.objects.filter(user=instance).last()
        
        
            # subject="Email Verification"
            # message = f"""
                            
            #                         <p>Hi {instance.username}, here is your OTP:  <strong>{otp.otp_code}</strong>.</p>
            #                         <p>It expires in 5 minutes. Please use the following URL to verify your email:</p>
            #                         <p><a href="http://127.0.0.1:8000/verify-email/{instance.username}">Verify Email</a></p>
                               
                                    
            #                         """
            # sender = "forexadim@gmail.com"
            # receiver = [instance.email ]
            
        
            
            
            # # send email
            # send_mail(
            #         subject,
            #         message,
            #         sender,
            #         receiver,
            #         fail_silently=False,
            #     )
            subject = "Email Verification"

            # Render the email content from the template
            html_message = render_to_string('authentication/email_verification.html', {
                'username': instance.username,
                'otp_code': otp.otp_code,
                'verification_url': f'https://vis-kxlh.onrender.com/users/verify-email/{instance.username}',
            })

            # Strip HTML tags to generate text content
            text_message = strip_tags(html_message)

            # Set sender, receiver, and other email parameters
            sender_email = "forexadim@gmail.com"
            receiver_email = [instance.email]

            # Send email
            send_mail(
                subject,
                text_message,  # Use text content for the email body
                sender_email,
                receiver_email,
                html_message=html_message,  # Attach HTML content for better formatting
                fail_silently=False,
            )
    
