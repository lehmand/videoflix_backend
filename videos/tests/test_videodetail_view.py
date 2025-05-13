from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from videos.models import Video
from videos.api.serializers import VideoListSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
import mock

class VideoDetailViewTest(TestCase):
    @mock.patch('django_rq.get_queue')
    def setUp(self, mock_get_queue):
        mock_queue = mock.MagicMock()
        mock_get_queue.return_value = mock_queue

        self.client = APIClient()
        
        self.video_file = SimpleUploadedFile(
            name='test_video.mp4',
            content=b'file_content',
            content_type='video/mp4'
        )
        
        self.thumbnail_file = SimpleUploadedFile(
            name='test_thumbnail.jpg',
            content=b'thumbnail_content',
            content_type='image/jpeg'
        )
        
        self.video = Video.objects.create(
            title="Test Video",
            description="This is a test video",
            file=self.video_file,
            thumbnail=self.thumbnail_file,
            genre="Action"
        )
        
        self.video_detail_url = reverse('video-detail', kwargs={'pk': self.video.pk})
        
        self.nonexistent_video_url = reverse('video-detail', kwargs={'pk': 999})

    def test_get_existing_video(self):
        """Test retrieving an existing video returns the correct data"""
        response = self.client.get(self.video_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['id'], self.video.id)
        self.assertEqual(response.data['title'], self.video.title)
        self.assertEqual(response.data['description'], self.video.description)
        self.assertIn('file', response.data)
        self.assertIn('thumbnail', response.data)
        self.assertEqual(response.data['genre'], self.video.genre)
        self.assertIn('uploaded_at', response.data)
        self.assertIn('updated_at', response.data)
        
    def test_get_nonexistent_video(self):
        """Test retrieving a non-existent video returns 404"""
        response = self.client.get(self.nonexistent_video_url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_serializer_works_with_single_instance(self):
        """Test that the serializer works correctly with a single video instance"""
        serializer = VideoListSerializer(self.video)
        
        self.assertEqual(serializer.data['id'], self.video.id)
        self.assertEqual(serializer.data['title'], self.video.title)
        self.assertEqual(serializer.data['description'], self.video.description)
        self.assertIn('file', serializer.data)
        self.assertIn('thumbnail', serializer.data)
        self.assertEqual(serializer.data['genre'], self.video.genre)
        self.assertIn('uploaded_at', serializer.data)
        self.assertIn('updated_at', serializer.data)
    
    @mock.patch('videos.api.views.get_object_or_404')
    def test_get_object_or_404_is_called(self, mock_get_object_or_404):
      """Test that get_object_or_404 is called with the correct arguments"""
      mock_get_object_or_404.return_value = self.video
      
      response = self.client.get(self.video_detail_url)
      
      mock_get_object_or_404.assert_called_once_with(Video, pk=self.video.pk)
      
      self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_method_not_allowed(self):
        """Test that methods other than GET are not allowed"""
        response = self.client.post(self.video_detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.put(self.video_detail_url, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.delete(self.video_detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)