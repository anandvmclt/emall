#emall/orders/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('order-list/', OrdersListCreateView.as_view(), name="order-list"),
    path('order-details/<str:uuid>/', OrdersDetailsAPIView.as_view(), name="order-details"),
    path('change-status/<str:uuid>/', ChangeOrderStatusView.as_view(), name="change-status"),
]