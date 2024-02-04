from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.wallet.models import walletsettings, wallet
from django.contrib import messages

from .models import *

def index(request):

  context = {
    'segment': 'dashboard',
  }
  return render(request, "dashboard/index.html", context)

def starter(request):

  context = {}
  return render(request, "pages/starter.html", context)

@login_required(login_url='/users/signin/')
def dashboard(request):
    return render(request, "dashboard/dashboard.html")
  
@login_required(login_url='/users/signin/')
def trade(request):
    return render(request, "dashboard/trade.html")

def deposit(request):
   wallet_settings = walletsettings.objects.first()
   print(wallet_settings)
   return render(request,"dashboard/deposit.html", {"wallet_settings":wallet_settings} )

def withdrawal(request):
   return(request, "dashboard/withdrawal.html")
 
def plan(request):
    if request.method == "POST":
        # Assuming your form has unique names for each button
        button_name = request.POST.get('button')

        if button_name == 'button1':
            amount = 1000
        elif button_name == 'button2':
            amount = 3000
        elif button_name == 'button3':
            amount = 5000
        else:
            amount = 0  # Default value if the button name is not recognized

        user_wallet = wallet.objects.get(user=request.user)
        
        # Check if the user has sufficient balance
        if user_wallet.wallet_balance >= amount:
            # Process the transaction
            user_wallet.wallet_balance -= amount
            user_wallet.save()
            
            # Add a success message
            messages.success(request, f"Successfully invested ${amount}.")

        else:
            # Add an error message if there are insufficient funds
            messages.error(request, "Insufficient funds to invest.")
        
        # Redirect to the same page to display the messages
        return redirect('plan')

    return render(request, "dashboard/plan.html")




