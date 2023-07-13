from dataclasses import fields
import email
from unittest import mock
from .models import User, Profile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import json

# from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'firstname', 'lastname']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, data):
        return User.objects.create_user(
            email=data.get("email"),
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
            password=data.get("password")
        )



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname',"email"]

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    image_url = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        fields = [ 'address', 'organization', 'zipcode', 'timezone','state', 'country','Phone','created_at','updated_at', 'user', 'image_url']
