from authentication.jwt_module import jwt_decode, jwt_encode
from authentication.models import UserInvitation, UserProfile
from authentication.Util import Util , generate_otp
from django.contrib.auth import authenticate
from django.db.models import Q
from django.http.response import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (ResetPasswordSerializer, UserInvitationSerializer,
                          UserLoginSerializer, UserRegistrationSerializer)


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
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        role = None

        if email:
            try:
                invitation = UserInvitation.objects.get(email=email, status=UserInvitation.PENDING)
                role = invitation.role
                serializer.validated_data['user_type_choice'] = role

                invitation.status = UserInvitation.ACCEPTED
                invitation.save()
            except UserInvitation.DoesNotExist:
                # No valid invitation found, proceed with registration without setting the role
                pass

        # If no role is fetched from the invitation, set the user_type_choice to "3" (Customer User)
        if not role:
            serializer.validated_data['user_type_choice'] = '3'
        
        user = serializer.save()
        data = serializer.data
        response = status.HTTP_200_OK 

        return Response(data, status=response)


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
            print(email, password)
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                if UserProfile.objects.get(email=request.data['email']).is_active:
                    token = get_tokens_for_user(
                        UserProfile.objects.get(email=request.data['email']))
                    return Response({'token': token, 'message': 'Login Successful', "User_id": UserProfile.objects.get(email=request.data['email']).id, "User_name": user.username}, status=status.HTTP_200_OK)

            else:
                return Response({'errors': 'Email or Password is not Valid'},
                                status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            # Handle the error here
            return Response({'errors': 'User does not exist'},
                            status=status.HTTP_404_NOT_FOUND)


class SendInvitationView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        """View for getting list of user whose invitation is pending or expired 

        Args:
            request (_type_): _description_
        """
        invited_by_user = request.user
        if invited_by_user.user_type_choice == "1" or "2":
            user_list = UserInvitation.objects.filter(
                Q(status=UserInvitation.PENDING) | Q(status=UserInvitation.EXPIRED), invited_by=invited_by_user)
            users_data = [{'id': user.id, 'email': user.email,
                           'status': user.status} for user in user_list]
            return JsonResponse(users_data, safe=False)
        else:
            return JsonResponse({'message': 'You are not authorized to access this data.'})

    @extend_schema(
        request=UserInvitationSerializer,
        responses={201: UserInvitationSerializer},
    )
    def post(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            if UserProfile.objects.filter(email=email):
                return JsonResponse({"message": "User is already registered."})
            
            invited_by_user = request.user  # Assuming you are using your custom User model
            if invited_by_user.user_type_choice == "3":
                return JsonResponse({"message": "You don't have enough privileges"})

            if invited_by_user.user_type_choice == "1":
                role = UserInvitation.ROLE_ADMIN
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
                        "website_url": "http://127.0.0.1/auth/register/",
                        "email_to": existing_user_invitation.email,
                        "email_subject": "User invitation",
                        "role": role
                    }
                    Util.send_mail(data)
                    # request.session['email_to'] = existing_user_invitation.email

                    return JsonResponse({"message": "User already exists but the previous invitation expired. A new invitation has been sent."}, status=200)
            except UserInvitation.DoesNotExist:
                pass

            user_invitation = UserInvitation.objects.create(
                email=email, status=UserInvitation.PENDING, invited_by=invited_by_user, role=role)
            user_invitation.save()

            data = {
                "website_url": "http://127.0.0.1/auth/register/",
                "email_to": user_invitation.email,
                "email_subject": "User invitation",
                "role": role
            }
            Util.send_mail(data)

            request.session['email_to'] = user_invitation.email

            return JsonResponse({"message": f"Invite Sent to {user_invitation.email}"}, status=200)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={201: ResetPasswordSerializer},
    )
    def post(self, request):
        email = request.data.get('email')
        if not UserProfile.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email Does not exists"})

        user = UserProfile.objects.get(email=email)
        otp = generate_otp()
        user.otp = otp
        user.save()

        data_send = {
            "website_url": "http://127.0.0.1:8000/auth",  # Replace with your website URL
            "email_to": email,
            "email_subject": "Reset your password",
            "otp": otp,
        }
        Util.send_reset_mail(data_send)

        return JsonResponse({"message": "Password reset email sent successfully"})


class ResetPasswordWithOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not email or not otp or not new_password or not confirm_password:
            return JsonResponse({"error": "Please provide all required data."}, status=400)

        try:
            user = UserProfile.objects.get(email=email, otp=otp)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "Invalid email or OTP."}, status=400)

        if new_password != confirm_password:
            return JsonResponse({"error": "Passwords do not match."}, status=400)

        # Reset the password
        user.set_password(confirm_password)
        user.otp = None
        user.save()

        return JsonResponse({"message": "Password reset successfully."})
