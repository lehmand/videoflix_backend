from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APIClient
from rest_framework import status
from user_auth.models import User
from unittest.mock import patch

class PasswordResetRequestViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.reset_url = reverse('password_reset')
        
        self.user_email = 'resetuser@example.com'
        self.user = User.objects.create_user(
            email=self.user_email,
            username=self.user_email,
            password='testpassword123'
        )
        
        self.non_existing_email = 'nonexistinguser@example.com'
        
        self.frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:4200')

    @patch('user_auth.api.views.send_reset_mail')
    def test_reset_request_existing_user(self, mock_send_mail):
        """Test password reset request for an existing user"""
        data = {'email': self.user_email}
        response = self.client.post(self.reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        mock_send_mail.assert_called_once()
        
        call_args = mock_send_mail.call_args[0]
        self.assertEqual(call_args[0], self.user_email)  # Email recipient
        self.assertEqual(call_args[1], self.user_email)  # Username
        
        reset_link = call_args[2]
        self.assertTrue(reset_link.startswith(f"{self.frontend_url}/reset/"))
        
        path_parts = reset_link.split('/')
        uid = path_parts[-2]
        token = path_parts[-1]
        
        decoded_uid = force_bytes(urlsafe_base64_encode(force_bytes(self.user.pk)))
        self.assertEqual(force_bytes(uid), decoded_uid)
        
        self.assertTrue(default_token_generator.check_token(self.user, token))

    @patch('user_auth.api.views.send_reset_mail')
    def test_reset_request_non_existing_user(self, mock_send_mail):
        """Test password reset request for a non-existing user"""
        data = {'email': self.non_existing_email}
        response = self.client.post(self.reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        mock_send_mail.assert_not_called()

    @patch('user_auth.api.views.send_reset_mail')
    def test_reset_request_with_empty_email(self, mock_send_mail):
        """Test password reset request with empty email"""
        data = {'email': ''}
        response = self.client.post(self.reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        mock_send_mail.assert_not_called()

    @patch('user_auth.api.views.send_reset_mail')
    def test_reset_request_without_email_parameter(self, mock_send_mail):
        """Test password reset request without email parameter"""
        data = {}
        response = self.client.post(self.reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        mock_send_mail.assert_not_called()

    @patch('user_auth.api.views.send_reset_mail')
    def test_reset_request_with_case_insensitive_email(self, mock_send_mail):
        """Test password reset request with case-insensitive email"""
        data = {'email': self.user_email.upper()}
        response = self.client.post(self.reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        if User.objects.filter(email__iexact=self.user_email.upper()).exists():
            mock_send_mail.assert_called_once()
        else:
            mock_send_mail.assert_not_called()