from django.urls import path, include
from .views import RegisterView, CustomAuthToken, CheckUserView, ActivateAccountView, PasswordResetConfirmView, PasswordResetRequestView

urlpatterns = [
  path('registration/', RegisterView.as_view(), name='registration'),
  path('login/', CustomAuthToken.as_view(), name='login'),
  path('check/', CheckUserView.as_view(), name='check'),
  path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
  path('reset/', PasswordResetRequestView.as_view(), name='password_reset'),
  path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]