#emall/user/serializers.py

from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


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
        

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if 'new_password' in data and 'old_password' in data:
            if data['new_password'] == data['old_password']:
                raise serializers.ValidationError("New password should not be the same as the old password.")
        return data

    def update(self, instance, validated_data):
        if 'new_password' in validated_data:
            old_password = validated_data.get('old_password')
            if not instance.check_password(old_password):
                raise serializers.ValidationError("Incorrect old password.")

            new_password = validated_data.get('new_password')
            validate_password(new_password, user=instance)
            instance.set_password(new_password)
            instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'user_scope']