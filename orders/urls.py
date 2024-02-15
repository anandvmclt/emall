#emall/orders/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('order-list/', OrdersListCreateView.as_view(), name="order-list"),
    path('order-details/<int:pk>/', OrdersDetailsAPIView.as_view(), name="order-details"),
]