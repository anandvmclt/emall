#emall/orders/views.py
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.rbac import IsAdmin, IsGetOrAdmin
# Create your views here.

def index(request):
    return JsonResponse({"message": "Welcome !"})

# Create your views here.
