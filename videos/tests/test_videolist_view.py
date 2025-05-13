from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from videos.models import Video
from videos.api.serializers import VideoListSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.dispatch import Signal
from django.test.utils import override_settings
import mock

class VideoListViewTest(TestCase):
    @mock.patch('django_rq.get_queue')
    def setUp(self, mock_get_queue):
        mock_queue = mock.MagicMock()
        mock_get_queue.return_value = mock_queue

        self.client = APIClient()
        self.video_list_url = reverse('video-list')
        
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
        
        self.video1 = Video.objects.create(
            title="Test Video 1",
            description="Description 1",
            file=self.video_file,
            thumbnail=self.thumbnail_file,
            genre="Action"
        )
        
        self.video2 = Video.objects.create(
            title="Test Video 2",
            description="Description 2",
            file=self.video_file,
            thumbnail=self.thumbnail_file,
            genre="Comedy"
        )
        
        self.video3 = Video.objects.create(
            title="Test Video 3",
            description="Description 3",
            file=self.video_file,
            thumbnail=self.thumbnail_file,
            genre="Drama"
        )
        
        self.videos = [self.video1, self.video2, self.video3]

    def tearDown(self):
        Video.objects.all().delete()
    
    def test_get_all_videos(self):
        """Test that the view returns all videos"""
        response = self.client.get(self.video_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 3)
        
        expected_titles = set(video.title for video in self.videos)
        response_titles = set(video['title'] for video in response.data)
        self.assertEqual(expected_titles, response_titles)
    
    def test_video_list_structure(self):
        """Test the structure of the returned video list"""
        response = self.client.get(self.video_list_url)
        
        self.assertIsInstance(response.data, list)
        
        first_video = response.data[0]
        self.assertIn('id', first_video)
        self.assertIn('title', first_video)
        self.assertIn('description', first_video)
        self.assertIn('file', first_video)
        self.assertIn('thumbnail', first_video)
        self.assertIn('genre', first_video)
        self.assertIn('uploaded_at', first_video)
        self.assertIn('updated_at', first_video)
        
    def test_serializer_fields(self):
        """Test that the serializer includes all expected fields"""
        serializer = VideoListSerializer(self.videos, many=True)
        
        self.assertEqual(len(serializer.data), 3)
        
        first_serialized_video = serializer.data[0]
        self.assertIn('id', first_serialized_video)
        self.assertIn('title', first_serialized_video)
        self.assertIn('description', first_serialized_video)
        self.assertIn('file', first_serialized_video)
        self.assertIn('thumbnail', first_serialized_video)
        self.assertIn('genre', first_serialized_video)
        self.assertIn('uploaded_at', first_serialized_video)
        self.assertIn('updated_at', first_serialized_video)
    
    @mock.patch('django_rq.get_queue')  # Mock RQ again for this test
    def test_empty_video_list(self, mock_get_queue):
        """Test that an empty list is returned when no videos exist"""
        mock_queue = mock.MagicMock()
        mock_get_queue.return_value = mock_queue
        
        Video.objects.all().delete()
        
        response = self.client.get(self.video_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])