from authentication.models import UserProfile, UserInvitation
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.http.response import JsonResponse
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from authentication.Util import Util

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
        permission_classes = [AllowAny, ]

        password = request.POST.get('password', None)

        confirm_password = request.POST.get('confirm_password', None)
        if password == confirm_password:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED
        else:
            data = ''
            raise ValidationError(
                {'password_mismatch': 'Password fields didn not match.'})

        return Response(data, status=response)



    # def post(self, request):
    #     print(request.data)
    #     if request.data.get("password") == request.data.get("confirm_password"):
    #         print(55555555555555555555555555555555)
    #         serializer = UserRegistrationSerializer(data=request.data)
    #         if serializer.is_valid(raise_exception=True):
    #             obj = serializer.save()
    #             return Response(data={'msg': 'Registration Successful', "id": obj.id},
    #                             status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(data={"message": "password is different"}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny, ]
    @extend_schema(
        request=UserLoginSerializer,
        responses={201: UserLoginSerializer},
    )
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
                if UserProfile.objects.get(email=request.data['email']).is_active:
                        token = get_tokens_for_user(UserProfile.objects.get(email=request.data['email']))
                        return Response({'token': token, 'message': 'Login Successful',"User_id":UserProfile.objects.get(email=request.data['email']).id,"User_name":user.username}, status=status.HTTP_200_OK)
               
            else:
                return Response({'errors': 'Email or Password is not Valid'},
                                status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
    # Handle the error here
            return Response({'errors': 'User does not exist'},
                                status=status.HTTP_404_NOT_FOUND)


class SendInvitationView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        """Method for inviting user"""
        if request.method == 'POST':
            email = request.data.get('email')
            invited_by_user = request.user  # Assuming you are using your custom User model

            if invited_by_user.user_type_choice == "1":
                role = UserInvitation.ROLE_TENANT_ADMIN
            else:
                role = UserInvitation.ROLE_USER

            if not email:
                return JsonResponse({"message": "Email field is required."}, status=400)

            try:
                existing_user_invitation = UserInvitation.objects.get(
                    email=email)
                if existing_user_invitation.status == UserInvitation.PENDING:
                    return JsonResponse({"message": "User already exists and invitation is pending."}, status=400)
                elif existing_user_invitation.status == UserInvitation.EXPIRED:
                    # Update the invitation status to pending and resend the invitation
                    existing_user_invitation.status = UserInvitation.PENDING
                    existing_user_invitation.save()

                    data = {
                        "website_url": "http://127.0.0.1/",
                        "email_to": existing_user_invitation.email,
                        "email_subject": "User invitation",
                        "role": role
                    }
                    Util.send_mail(data)

                    request.session['email_to'] = existing_user_invitation.email

                    return JsonResponse({"message": "User already exists but the previous invitation expired. A new invitation has been sent."}, status=200)
            except UserInvitation.DoesNotExist:
                pass

            user_invitation = UserInvitation.objects.create(
                email=email, status=UserInvitation.PENDING, invited_by=invited_by_user, role=role)
            user_invitation.save()

            data = {
                "website_url": "http://127.0.0.1/",
                "email_to": user_invitation.email,
                "email_subject": "User invitation",
                "role": role
            }
            Util.send_mail(data)

            request.session['email_to'] = user_invitation.email

            return JsonResponse({"message": f"Invite Sent to {user_invitation.email}"}, status=200)



