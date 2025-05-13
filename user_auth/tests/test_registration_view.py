from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user_auth.models import User

class RegistrationViewTest(TestCase):
  def setUp(self):
    self.client = Client()

    self.registration_url = reverse('registration')

    self.valid_user_data = {
      'email': 'validuser@example.com',
      'password': 'testpassword123',
      'repeated_password': 'testpassword123'
    }

  def test_registration_success(self):
    '''Test successful registration with valid data'''

    response = self.client.post(self.registration_url, self.valid_user_data, content_type='application/json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn('token', response.data)
    self.assertIn('user_id', response.data)
    self.assertEqual(response.data['email'], self.valid_user_data['email'])

    self.assertTrue(User.objects.filter(email=self.valid_user_data['email']).exists())
    user = User.objects.get(email=self.valid_user_data['email'])
    self.assertEqual(user.username, self.valid_user_data['email'])
    self.assertFalse(user.is_activated)

  def test_registration_password_mismatch(self):
        """Test registration fails when passwords don't match"""
        data = self.valid_user_data.copy()
        data['repeated_password'] = 'different_password'
        
        response = self.client.post(self.registration_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(User.objects.filter(email=data['email']).exists())

  def test_registration_duplicate_email(self):
        """Test registration fails with duplicate email"""
        User.objects.create_user(
            email=self.valid_user_data['email'],
            username=self.valid_user_data['email'],
            password=self.valid_user_data['password']
        )
        
        response = self.client.post(self.registration_url, self.valid_user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

  def test_registration_invalid_email(self):
        """Test registration fails with invalid email format"""
        data = self.valid_user_data.copy()
        data['email'] = 'invalid-email'
        
        response = self.client.post(self.registration_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

  def test_registration_short_password(self):
        """Test registration fails with too short password"""
        data = self.valid_user_data.copy()
        data['password'] = 'short'
        data['repeated_password'] = 'short'
        
        response = self.client.post(self.registration_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('Password must be at least 6 characters long.', response.data['password'])
        self.assertFalse(User.objects.filter(email=data['email']).exists())

  def test_registration_missing_fields(self):
        """Test registration fails with missing required fields"""
        data = {
            'password': self.valid_user_data['password'],
            'repeated_password': self.valid_user_data['repeated_password']
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {
            'email': self.valid_user_data['email'],
            'repeated_password': self.valid_user_data['repeated_password']
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {
            'email': self.valid_user_data['email'],
            'password': self.valid_user_data['password']
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

