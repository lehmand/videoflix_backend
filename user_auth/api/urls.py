from django.urls import path, include
from .views import RegisterView, CustomAuthToken

urlpatterns = [
  path('registration/', RegisterView.as_view(), name='registration'),
  path('login/', CustomAuthToken.as_view(), name='login'),
]