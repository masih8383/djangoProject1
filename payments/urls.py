from django.urls import path
from .views import GatewayView,PaymentView



urlpatterns = [
    path('',GatewayView.as_view(),name='geteway'),
    path('',PaymentView.as_view(),name='payment'),
]