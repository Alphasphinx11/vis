from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.wallet.models import walletsettings, wallet, Withdrawal, Deposit
from django.contrib import messages
from django.contrib.auth.models import User
from decimal import Decimal

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
    user_wallet = wallet.objects.get(user=request.user)
    context = {
        'user_wallet': user_wallet
    }
    return render(request, "dashboard/dashboard.html", context)
  
@login_required(login_url='/users/signin/')
def trade(request):
    return render(request, "dashboard/trade.html")

@login_required(login_url='/users/signin/')
def deposit(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        user = request.user
        wallet = user.wallet  # Retrieve the user's wallet
        deposit = Deposit.objects.create(user=user, wallet=wallet, amount=amount)
        messages.success(request, 'Deposit sent successfully! Awaiting approval.')
        
        # Redirect to the dashboard
        return redirect('dashboard')
    
    # Get wallet settings
    wallet_settings = walletsettings.objects.first()
    
    # Render the deposit template with wallet settings
    return render(request, 'dashboard/deposit.html', {'wallet_settings': wallet_settings})

@login_required
def withdrawal(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount', 0))
        wallet_address = request.POST.get('wallet_address', '')
        
        # Ensure the withdrawal charges are represented as Decimal
        withdrawal_charges = Decimal('0.20') * amount

        # Subtract withdrawal charges from the withdrawal amount
        total_amount = amount - withdrawal_charges
        user_wallet = request.user.wallet
        # Check if user has sufficient balance
        if total_amount > user_wallet.wallet_balance:
            # Display error message for insufficient funds
            messages.error(request, 'Insufficient funds for withdrawal.')
            return redirect('dashboard')  # Redirect to dashboard or wherever appropriate
        
        user_wallet.wallet_balance -= total_amount
        user_wallet.save()
        # Save withdrawal request
        withdrawal_request = Withdrawal.objects.create(
            user=request.user,
            wallet=user_wallet,
            amount=amount,
            walletAddress=wallet_address,
        )

        # Display success message
        messages.success(request, 'Withdrawal request sent successfully.')
        return redirect('dashboard')  # Assuming you have a URL named 'dashboard'

    return render(request, "dashboard/withdrawal.html")
@login_required 
def plan(request):
    if request.method == "POST":
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
        
        if user_wallet.wallet_balance >= amount:
            # Deduct the amount from the wallet balance
            user_wallet.wallet_balance -= amount
            # Add the deducted amount to the trade balance
            user_wallet.trade_balance += amount
            user_wallet.save()
            
            messages.success(request, f"Successfully invested ${amount}.")

        else:
            messages.error(request, "Insufficient funds to trade, make a deposit")
        
        return redirect('dashboard')

    return render(request, "dashboard/plan.html")

@login_required
def transfer(request):
    if request.method =="POST":
        user_wallet = wallet.objects.get(user=request.user)

        amount_str = request.POST.get("Trade_amount")
        amount = Decimal(amount_str)
        if amount > user_wallet.trade_balance:
            messages.error(request, "Insufficient funds, place a Trade first")
        else:
            messages.success(request, "successfully transfered funds to wallet")

            user_wallet.trade_balance -= amount
            user_wallet.wallet_balance += amount

            user_wallet.save()
        return redirect('dashboard') 
    return render(request, "dashboard/transfer.html")







