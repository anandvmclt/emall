from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category,Product
from .serializer import ProductSerializer, CategorySerializer
from user.rbac import IsAdmin, IsGetOrAdmin
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
# Create your views here.



def index(request):
    return JsonResponse({"message": "Welcome !"})


# List and create new Category
class CategoryListCreateView(ListCreateAPIView):
    permission_classes = (IsGetOrAdmin,)
    queryset = Category.objects.filter(is_deleted=False, status=True).order_by('-id')
    serializer_class = CategorySerializer


class CategoryDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsGetOrAdmin,)
    queryset = Category.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = CategorySerializer



# List and create products
class ProductListCreateView(ListCreateAPIView):
    permission_classes = (IsGetOrAdmin,)
    queryset = Product.objects.filter(is_deleted=False, status=True).order_by('-id')
    serializer_class = ProductSerializer


class ProductDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsGetOrAdmin,)
    queryset = Product.objects.filter(is_deleted=False).order_by('-id')
    serializer_class = ProductSerializer


class ProductListView(APIView):
    # Use the cache_page decorator to cache the API response for 60 seconds
    @cache_page(60)
    def get(self, request):
        try:
            # Check if the data is already in the cache
            cached_data = cache.get('product_list')
            if cached_data:
                return Response(cached_data)

            # If not in cache, fetch the data from the database
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)

            # Store the data in the cache for future requests
            cache.set('product_list', serializer.data, 60)

            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Cashing explanations.
""" 
We import cache and cache_page from Django.
The ProductListView class is a Django class-based view for listing products.
The @cache_page(60) decorator caches the response for 60 seconds.
We check if the data is already in the cache using cache.get('product_list').
If the data is in the cache, we return the cached data.
If not in the cache, we fetch the data from the database, serialize it, and store 
it in the cache using cache.set('product_list', serializer.data, 60).
The cached data is then returned as the API response.

BACKEND: Specifies the cache backend to use. In this case, we're using 
django.core.cache.backends.locmem.LocMemCache for the local memory cache.

LOCATION: A unique identifier for the local memory cache. It can be any string;
 we're using 'unique-snowflake'.

CACHE_TIMEOUT: Specifies the default cache timeout for API responses.
 This value is in seconds. In the example, it's set to 60 seconds.

"""

# Swagger Documentation