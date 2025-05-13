from rest_framework import serializers
from videos.models import Video

class VideoListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model that converts Video instances to and from JSON.
    
    This serializer handles the conversion of Video model instances to JSON for API responses
    and the parsing of incoming JSON data for creating or updating Video instances. It includes
    all fields from the Video model without any customization or additional validation.
    """
    class Meta:
        """
        Meta configuration for the VideoListSerializer.
        
        Specifies:
        - model: The model class to serialize (Video)
        - fields: Which fields to include in the serialized output ('__all__' includes all model fields)
          Including: id, title, description, file, thumbnail, genre, uploaded_at, updated_at
        """
        model = Video
        fields = '__all__'  # Includes all fields from the Video model
 