from rest_framework import serializers
from videos.models import Video

class VideoListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Video
    fields = '__all__'
 