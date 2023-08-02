from .models import UserProfile, Profile, UserInvitation
from rest_framework import serializers
from django.contrib.auth import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'password','server']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserProfile(**validated_data)
        user.set_password(password)
        user.save()
        return user

    # class Meta:
    #     model = UserProfile
    #     fields = ['email', 'password', 'password2', 'username']
    #     extra_kwargs = {
    #         'password': {'write_only': True}
    #     }
    #
    # def create(self, data):
    #     return UserProfile.objects.create_user(
    #         email=data.get("email"),
    #         firstname=data.get("firstname"),
    #         lastname=data.get("lastname"),
    #         password=data.get("password")
    #     )


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = UserProfile
        fields = ['email', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    image_url = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['address', 'organization', 'zipcode', 'timezone', 'state',
                  'country', 'Phone', 'created_at', 'updated_at', 'user', 'image_url']


class UserInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInvitation
        fields = ["email"]  # Include only the 'email' field


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    
