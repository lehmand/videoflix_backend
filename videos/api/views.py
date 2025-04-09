from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from videos.models import Video
from .serializers import VideoListSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoListView(APIView):
  @method_decorator(cache_page(CACHE_TTL))
  def get(self, request):
    videos = Video.objects.all()
    serializer = VideoListSerializer(videos, many=True)

    return Response(serializer.data)