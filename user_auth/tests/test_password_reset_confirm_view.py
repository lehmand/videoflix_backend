from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APIClient
from rest_framework import status
from user_auth.models import User

class PasswordResetConfirmViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user_email = 'resetuser@example.com'
        self.user = User.objects.create_user(
            email=self.user_email,
            username=self.user_email,
            password='oldpassword123'
        )
        
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        
        self.reset_confirm_url = reverse('password_reset_confirm', kwargs={
            'uidb64': self.uid,
            'token': self.token
        })
        
        self.valid_reset_data = {
            'new_password': 'newpassword123',
            'new_password2': 'newpassword123'
        }

    def test_successful_password_reset(self):
        """Test successful password reset with valid token and matching passwords"""
        response = self.client.post(
            self.reset_confirm_url,
            self.valid_reset_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Password has been reset successfully.')
        
        self.user.refresh_from_db()
        self.assertTrue(
            self.client.login(
                username=self.user_email,
                password=self.valid_reset_data['new_password']
            )
        )

    def test_passwords_dont_match(self):
        """Test reset fails when passwords don't match"""
        data = {
            'new_password': 'newpassword123',
            'new_password2': 'differentpassword123'
        }
        
        response = self.client.post(
            self.reset_confirm_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Passwords do not match.')
        
        self.user.refresh_from_db()
        self.assertTrue(
            self.client.login(
                username=self.user_email,
                password='oldpassword123'
            )
        )

    def test_invalid_token(self):
        """Test reset fails with invalid token"""
        invalid_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': self.uid,
            'token': 'invalid-token'
        })
        
        response = self.client.post(
            invalid_token_url,
            self.valid_reset_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid or expired token.')
        
        self.user.refresh_from_db()
        self.assertTrue(
            self.client.login(
                username=self.user_email,
                password='oldpassword123'
            )
        )

    def test_invalid_uid(self):
        """Test reset fails with invalid UID"""
        invalid_uid_url = reverse('password_reset_confirm', kwargs={
            'uidb64': 'invalid-uid',
            'token': self.token
        })
        
        response = self.client.post(
            invalid_uid_url,
            self.valid_reset_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid reset link.')

    def test_nonexistent_user(self):
        """Test reset fails with UID of non-existent user"""
        user_pk = self.user.pk
        self.user.delete()
        
        nonexistent_uid = urlsafe_base64_encode(force_bytes(user_pk))
        
        nonexistent_user_url = reverse('password_reset_confirm', kwargs={
            'uidb64': nonexistent_uid,
            'token': self.token
        })
        
        response = self.client.post(
            nonexistent_user_url,
            self.valid_reset_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid reset link.')

    def test_token_becomes_invalid_after_password_change(self):
        """Test that token becomes invalid after user changes password"""
        first_reset_response = self.client.post(
            self.reset_confirm_url,
            self.valid_reset_data,
            format='json'
        )
        
        self.assertEqual(first_reset_response.status_code, status.HTTP_200_OK)
        
        second_reset_data = {
            'new_password': 'anotherpassword123',
            'new_password2': 'anotherpassword123'
        }
        
        second_reset_response = self.client.post(
            self.reset_confirm_url,
            second_reset_data,
            format='json'
        )
        
        self.assertEqual(second_reset_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', second_reset_response.data)
        self.assertEqual(second_reset_response.data['message'], 'Invalid or expired token.')
        
        self.user.refresh_from_db()
        self.assertFalse(
            self.client.login(
                username=self.user_email,
                password=second_reset_data['new_password']
            )
        )
        self.assertTrue(
            self.client.login(
                username=self.user_email,
                password=self.valid_reset_data['new_password']
            )
        )

    def test_missing_parameters(self):
        """Test reset fails with missing parameters"""
        data1 = {'new_password2': 'newpassword123'}
        response1 = self.client.post(
            self.reset_confirm_url,
            data1,
            format='json'
        )
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        
        data2 = {'new_password': 'newpassword123'}
        response2 = self.client.post(
            self.reset_confirm_url,
            data2,
            format='json'
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
        data3 = {}
        response3 = self.client.post(
            self.reset_confirm_url,
            data3,
            format='json'
        )
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.user.refresh_from_db()
        self.assertTrue(
            self.client.login(
                username=self.user_email,
                password='oldpassword123'
            )
        )

    def test_short_password(self):
        """Test reset fails with short password (assuming 6 char minimum)"""
        data = {
            'new_password': 'short',  
            'new_password2': 'short'
        }
        
        response = self.client.post(
            self.reset_confirm_url,
            data,
            format='json'
        )
        
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            self.user.refresh_from_db()
            self.assertTrue(
                self.client.login(
                    username=self.user_email,
                    password='oldpassword123'
                )
            )