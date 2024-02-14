from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category,Product
from .serializer import ProductSerializer, CategorySerializer
from user.rbac import IsAdmin, IsGetOrAdmin
# Create your views here.



def index(request):
    return JsonResponse({"message": "Welcome !"})



class CategoryListCreateView(ListCreateAPIView):
    permission_classes = (IsGetOrAdmin,)
    queryset = Category.objects.filter(is_deleted=False, status=True).order_by('-id')
    serializer_class = CategorySerializer


class CategoryDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsGetOrAdmin,)
    queryset = Category.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = CategorySerializer