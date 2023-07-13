from django.http import Http404
import json
from authentication.models import User, Profile
from .serializers import UserRegistrationSerializer, UserLoginSerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate, logout
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import permissions
from django.contrib.auth.hashers import check_password




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    permission_classes = [AllowAny, ]

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer},
    )
    def post(self, request):
        if request.data.get("password") == request.data.get("password2"):
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                obj = serializer.save()
                return Response(data={'msg': 'Registration Successful', "id": obj.id},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "password is different"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        try:
            print(email,password)

            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
              
                if User.objects.get(email=request.data['email']).is_active:
                        token = get_tokens_for_user(User.objects.get(email=request.data['email']))
                        return Response({'token': token, 'message': 'Login Successful',"User_id":User.objects.get(email=request.data['email']).id,"User_name":user.firstname+" "+user.lastname,"is_admin":user.is_admin}, status=status.HTTP_200_OK)
               
            else:
                return Response({'errors': 'Email or Password is not Valid'},
                                status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
    # Handle the error here
            return Response({'errors': 'User does not exist'},
                                status=status.HTTP_404_NOT_FOUND)
