#emall/user/serializers.py

from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'email', 'first_name', 'last_name',
                  'mobile', 'user_scope','username')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True, 'required': True},
            'email': {'required': False},
            'mobile': {'required': True},
            'user_scope': {'required': False},
        }

    def create(self, validated_data):
        if 'username' not in validated_data:
            raise ValidationError({'username': 'This field is required'})
        return User.objects.create_user(**validated_data)
    

    # Logged user can see his profile on dashboard.
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'uuid', 'first_name', 'last_name', 'email', 'username',
                 'mobile', 'status','created_at')