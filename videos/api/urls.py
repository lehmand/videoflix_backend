from django.urls import path
from .views import VideoListView

urlpatterns = [
    path('video-page/', VideoListView.as_view(), name='video-list'),
]