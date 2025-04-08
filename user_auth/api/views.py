from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from .utils import generate_activation_link, send_confirm_mail

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
      token, _ = Token.objects.get_or_create(user=user)
      return Response({
        'user_id': user.pk,
        'email': user.email,
        'token': token.key
      }, status=HTTP_200_OK)
    else:
      return Response({'message': 'Invalid username or password.'}, status=HTTP_401_UNAUTHORIZED)



