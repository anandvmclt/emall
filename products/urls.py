#emall/products/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('',  index, name="index"),
    path('category-list',  CategoryListCreateView.as_view(), name="category-list"),
    path('category-details/<int:pk>',  CategoryDetailsAPIView.as_view(), name="category-details"),

]
