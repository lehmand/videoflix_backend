from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from videos.models import Video
from .serializers import VideoListSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoListView(APIView):
    # @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        """
        Handle GET requests for the video list.
        
        Retrieves all videos from the database, serializes them,
        and returns them as a JSON response.
        """
        videos = Video.objects.all()
        serializer = VideoListSerializer(videos, many=True)

        return Response(serializer.data)
  
class VideoDetailView(APIView):
    def get(self, request, pk):
        """
        Handle GET requests for a specific video.
        
        Retrieves a single video by its primary key, serializes it,
        and returns it as a JSON response. Returns 404 if the video is not found.
        """
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoListSerializer(video)
        
        return Response(serializer.data, status=status.HTTP_200_OK)