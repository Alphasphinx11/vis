from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.wallet.models import walletsettings, wallet, Withdrawal, Deposit
from django.contrib import messages
from django.contrib.auth.models import User
from decimal import Decimal 
from apps.users.decorators import kyc_verified_required
from apps.users.models import Kyc

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
@kyc_verified_required
def trade(request):
    return render(request, "dashboard/trade.html")

@login_required(login_url='/users/signin/')
@kyc_verified_required
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

@login_required(login_url='/users/signin/')
@kyc_verified_required
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

@login_required(login_url='/users/signin/') 
@kyc_verified_required
def plan(request):
    if request.method == "POST":
        button_name = request.POST.get('button')

        if button_name == 'button1':
            plan = "Bronze"
        elif button_name == 'button2':
            plan = "Silver"
        elif button_name == 'button3':
            plan = "Gold"
        else:
            plan = "None"  # Default value if the button name is not recognized

            
        messages.success(request, f"Successfully applied a ${plan} Strategy.")
        
        return redirect('trade')

    return render(request, "dashboard/plan.html")

@login_required(login_url='/users/signin/')
@kyc_verified_required
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


@login_required(login_url='/users/signin/')
def kyc_verification(request):
    user = request.user
    try:
        kyc_info = Kyc.objects.get(user=user)
    except Kyc.DoesNotExist:
        kyc_info = None

    if kyc_info and not kyc_info.verified:
        # If KYC information exists for the user but is not verified, redirect
        messages.info(request, "KYC information is pending verification.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        id_type = request.POST.get('id_type')
        pic = request.FILES.get('pic')
        selfie = request.FILES.get('selfie')
        
        if kyc_info:
            kyc_info.id_type = id_type
            if pic:
                kyc_info.pic = pic
            if selfie:
                kyc_info.selfie = selfie
            # Save the KYC information
            kyc_info.save()
            messages.success(request, "KYC information saved successfully, waiting for Verification.")
            return redirect('kyc')
        else:
            # Create a new KYC object if it doesn't exist
            kyc_info = Kyc.objects.create(user=user, id_type=id_type, pic=pic, selfie=selfie)
            messages.success(request, "KYC information saved successfully.")
            return redirect('dashboard')
    
    return render(request, 'authentication/kyc.html', {'kyc_info': kyc_info})

@login_required(login_url='/users/signin/')
@kyc_verified_required
def execute_trade(request):

    if request.method == 'POST':
        user_wallet = wallet.objects.get(user=request.user)
        # Process the form data
        symbol = request.POST.get('symbol')
        amount = request.POST.get('amount')
        profit = request.POST.get('profit')
        trade_type = request.POST.get('type')
        lot_size = request.POST.get('lot_size')
        duration = request.POST.get('duration')

        # Validate the form data
        if not symbol or not amount or not trade_type or not lot_size or not duration:
            messages.error(request, 'All fields are required.')
            return redirect('execute')

        # Check if the symbol and type are valid choices

        # Save the trade details to the database
        trade = Trade(
            user=request.user,
            symbol=symbol,
            amount=amount,
            type=trade_type,
            lot_size=lot_size,
            duration=duration,
            status='open'  # Assuming the initial status is 'open'
        )

        wallet_balance = request.user.wallet.wallet_balance
        

        amount_decimal = Decimal(amount)

        if amount_decimal > wallet_balance:
            # Add a message informing the user to deposit funds
            messages.error(request, 'Insufficient funds. Make a deposit to execute this trade.')
            
            # Redirect the user to the deposit page
            return redirect('deposit')
        
        else:
            user_wallet.wallet_balance -= amount_decimal
            user_wallet.trade_balance += amount_decimal

            user_wallet.save()

            trade.save()

        # Add success message
        messages.success(request, 'Trade executed successfully.')
        
        # Redirect to a success page or another URL
        return redirect('trade_history')
        
        # Redirect to a failure page or another URL
    return render(request, 'dashboard/popup.html')
   
@login_required(login_url='/users/signin/')
@kyc_verified_required
def trade_history(request):
     trades = Trade.objects.filter(user=request.user)

     return render(request, 'dashboard/trade_history.html', {'trades': trades})



