from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user_auth.models import User

class CheckUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.check_url = reverse('check')
        
        # Create a test user
        self.existing_user_email = 'existinguser@example.com'
        self.user = User.objects.create_user(
            email=self.existing_user_email,
            username=self.existing_user_email,
            password='password123'
        )
        
        # Non-existing user email for testing
        self.non_existing_email = 'nonexistinguser@example.com'

    def test_check_existing_user(self):
        """Test checking for an existing user returns ok=True"""
        data = {'email': self.existing_user_email}
        response = self.client.post(self.check_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ok', response.data)
        self.assertTrue(response.data['ok'])

    def test_check_non_existing_user(self):
        """Test checking for a non-existing user returns ok=False"""
        data = {'email': self.non_existing_email}
        response = self.client.post(self.check_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ok', response.data)
        self.assertFalse(response.data['ok'])

    def test_check_with_empty_email(self):
        """Test checking with an empty email returns ok=False"""
        data = {'email': ''}
        response = self.client.post(self.check_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ok', response.data)
        self.assertFalse(response.data['ok'])

    def test_check_without_email_parameter(self):
        """Test checking without providing an email parameter returns ok=False"""
        data = {}
        response = self.client.post(self.check_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ok', response.data)
        self.assertFalse(response.data['ok'])

    def test_check_with_case_insensitive_email(self):
        """Test checking with case-insensitive email (Django's default behavior)"""
        data = {'email': self.existing_user_email.upper()}
        response = self.client.post(self.check_url, data, format='json')
        
        # Django's default behavior is case-insensitive email comparison
        # This test verifies this behavior is maintained
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ok', response.data)
        self.assertTrue(response.data['ok'])