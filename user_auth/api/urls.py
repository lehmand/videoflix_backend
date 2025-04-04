from django.urls import path, include
from .views import RegisterView

urlpatterns = [
  path('registration/', RegisterView.as_view(), name='registration')
]