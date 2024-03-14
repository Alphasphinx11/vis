from django.shortcuts import redirect
from functools import wraps
from .models import Kyc

def kyc_verified_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if not authenticated
        
        # Check if the user has a KYC record
        try:
            kyc = Kyc.objects.get(user=request.user)
        except Kyc.DoesNotExist:
            return redirect('kyc')  # Redirect to KYC submission page if KYC record does not exist
        
        # Check if KYC is verified
        if not kyc.verified:
            return redirect('kyc')  # Redirect to pending KYC verification page
        
        # User has verified KYC, allow access to the view
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def email_verified_required(view_func):
    def email_wrapped_view(request, *args, **kwargs):
        try:
            pass
        except:
            pass