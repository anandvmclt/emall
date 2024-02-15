#emall/orders/serializer.py

from rest_framework import serializers
from .models import Orders
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"
        # Depth - Get all data from Related table
        # depth = 1


        
# ---------------------------- *NESTED SERIALIZERS*---------------------#
class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]



class OrderDetailSerializer(serializers.ModelSerializer):

    customer = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    class Meta:
        model = Orders
        fields = "__all__"

    def get_customer(self, obj):
        try:
            if obj.customer is not None:
                serializer  = UserNestedSerializer(obj.customer)
                return serializer.data
                # user = User.objects.get(id=obj.customer.id)
                # return user.username

            return None
        except Exception as ex:
            return None
        
    
    def get_product(self, obj):
        try:
            if obj.product:
                product = Product.objects.get(id=obj.product.id)
                return product.name
            return None
        except Exception as ex:
            return None