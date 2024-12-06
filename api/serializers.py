from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'identity_number', 'email', 'date_of_birth']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'identity_number', 'date_of_birth']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
