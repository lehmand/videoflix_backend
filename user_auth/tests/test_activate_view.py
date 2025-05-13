from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from user_auth.models import User

class ActivateAccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser@example.com',
            password='testpassword123',
            is_activated=False  
        )
        
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        
        self.valid_activation_url = reverse('activate', kwargs={
            'uidb64': self.uid,
            'token': self.token
        })

    def test_successful_activation(self):
        """Test successful account activation with valid token and UID"""
        response = self.client.get(self.valid_activation_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'redirect_pages/activation_success.html')
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_activated)
        
        self.assertEqual(
            response.context['frontend_url'], 
            getattr(settings, 'FRONTEND_URL', 'http://localhost:4200')
        )

    def test_invalid_token(self):
        """Test activation fails with invalid token"""
        invalid_token_url = reverse('activate', kwargs={
            'uidb64': self.uid,
            'token': 'invalid-token'
        })
        
        response = self.client.get(invalid_token_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'redirect_pages/activation_invalid.html')
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_activated)
        
        self.assertEqual(
            response.context['frontend_url'], 
            getattr(settings, 'FRONTEND_URL', 'http://localhost:4200')
        )

    def test_invalid_uid(self):
        """Test activation fails with invalid UID"""
        invalid_uid_url = reverse('activate', kwargs={
            'uidb64': 'invalid-uid',
            'token': self.token
        })
        
        response = self.client.get(invalid_uid_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'redirect_pages/activation_invalid.html')
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_activated)

    def test_nonexistent_user(self):
        """Test activation fails with UID of non-existent user"""
        user_pk = self.user.pk
        self.user.delete()
        
        nonexistent_uid = urlsafe_base64_encode(force_bytes(user_pk))
        
        nonexistent_user_url = reverse('activate', kwargs={
            'uidb64': nonexistent_uid,
            'token': self.token
        })
        
        response = self.client.get(nonexistent_user_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'redirect_pages/activation_invalid.html')

    def test_already_activated_user(self):
        """Test activation with already activated user still returns success"""
        self.user.is_activated = True
        self.user.save()
        
        response = self.client.get(self.valid_activation_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'redirect_pages/activation_success.html')
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_activated)

    def test_token_becomes_invalid_after_password_change(self):
        """Test that token becomes invalid after user password change"""
        self.user.set_password('newpassword123')
        self.user.save()
        
        response = self.client.get(self.valid_activation_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'redirect_pages/activation_invalid.html')
        
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_activated)