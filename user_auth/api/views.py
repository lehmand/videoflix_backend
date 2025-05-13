from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from user_auth.models import User
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from .serializers import RegisterSerializer
from .utils import generate_activation_link, send_confirm_mail, send_reset_mail

class RegisterView(generics.CreateAPIView):
  serializer_class = RegisterSerializer
  permission_classes = [AllowAny]

  def create(self, request):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      token, _ = Token.objects.get_or_create(user=user)
      activation_link = generate_activation_link(user)
      send_confirm_mail(user.email, user.username, activation_link)

      return Response({
        'user_id': user.id,
        'email': user.email,
        'token': token.key
      }, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
  
class CustomAuthToken(ObtainAuthToken):
  permission_classes = [AllowAny]

  def post(self, request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)
    if user is not None:
      if not user.is_activated:
        return Response(
           {'message': 'Account not activated. Please activate your account via the email activation link.'},
            status=HTTP_401_UNAUTHORIZED
          )
      token, _ = Token.objects.get_or_create(user=user)
      return Response({
        'user_id': user.pk,
        'email': user.email,
        'token': token.key
      }, status=HTTP_200_OK)
    else:
      return Response({'message': 'Invalid username or password.'}, status=HTTP_401_UNAUTHORIZED)


class CheckUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '')
        exists = User.objects.filter(email__iexact=email).exists()
        return Response({'ok': exists}, status=HTTP_200_OK)
    
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            user = None

        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:4200')
        context = {'frontend_url': frontend_url}

        if user is not None and default_token_generator.check_token(user, token):
            user.is_activated = True
            user.save()
            return render(request, 'redirect_pages/activation_success.html', context)
        else:
            return render(request, 'redirect_pages/activation_invalid.html', context)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({
                'message': 'If an account exists for the specified email, you will receive an email with password reset instructions.'
            }, status=HTTP_200_OK)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:4200')
        reset_link = f"{frontend_url}/reset/{uid}/{token}"
        
        send_reset_mail(user.email, user.username, reset_link)
        
        return Response({
            'message': 'If an account exists for the specified email, you will receive an email with password reset instructions.'
        }, status=HTTP_200_OK)
    
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, uidb64, token):
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')
        
        if not new_password or not new_password2:
            return Response(
                {'message': 'Both password fields are required.'},
                status=HTTP_400_BAD_REQUEST
            )
        
        if new_password != new_password2:
            return Response(
                {'message': 'Passwords do not match.'},
                status=HTTP_400_BAD_REQUEST
            )
            
        if len(new_password) < 6:
            return Response(
                {'message': 'Password must be at least 6 characters long.'},
                status=HTTP_400_BAD_REQUEST
            )
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response(
                {'message': 'Invalid reset link.'},
                status=HTTP_400_BAD_REQUEST
            )
        
        if not default_token_generator.check_token(user, token):
            return Response(
                {'message': 'Invalid or expired token.'},
                status=HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response(
            {'message': 'Password has been reset successfully.'},
            status=HTTP_200_OK
        )