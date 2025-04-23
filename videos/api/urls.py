from django.urls import path
from .views import VideoListView, VideoDetailView

urlpatterns = [
    path('video-page/', VideoListView.as_view(), name='video-list'),
    path('video-page/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
]