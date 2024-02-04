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
]
