from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("starter/", views.starter, name="starter"),
    path("dashboard/", views.dashboard, name = "dashboard"),
    path("deposit/", views.deposit, name = "deposit"),
    path("withdrawal/", views.withdrawal, name = "withdrawal"),
    path("trade/", views.trade, name= "trade"),
    path("plan/", views.plan, name= "plan"),
    path("transfer/", views.transfer, name= "transfer"),
    path("kyc_submit/", views.kyc_verification, name= "kyc"),
    path("execute/", views.execute_trade, name= "execute"),
    path("trade_history/", views.trade_history, name= "trade_history"),
    path("privacy/", views.privacy, name= "privacy"),
]
