from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user_auth.models import User

# Create your tests here.


class LoginViewTest(TestCase):
  def setUp(self):
    self.client = APIClient()

    self.user_data = {
      'email': 'testuser@example.com',
      'username': 'testuser@example.com',
      'password': 'testpassword123'
    }

    self.user = User.objects.create_user(**self.user_data)
    self.user.is_activated = True
    self.user.save()

    self.login_url = reverse('login')

  def test_login_success(self):
    '''Test login successful with correct data'''
    data = {
      'email': self.user_data['email'],
      'password': self.user_data['password']
    }

    response = self.client.post(self.login_url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('token', response.data)
    self.assertIn('user_id', response.data)
    self.assertEqual(response.data['email'], self.user_data['email'])

  def test_login_wrong_password(self):
    '''Test login failed with wrong password.'''
    data = {
      'email': self.user_data['email'],
      'password': 'wrongpassword'
    }

    response = self.client.post(self.login_url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertIn('message', response.data)
    self.assertEqual(response.data['message'], 'Invalid username or password.')

  def test_login_user_nonexistent(self):
    '''Test login failed with non existent user.'''
    data = {
      'email': 'superuser@gmail.com',
      'password': 'testpassword123'
    }

    response = self.client.post(self.login_url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertIn('message', response.data)
    self.assertEqual(response.data['message'], 'Invalid username or password.')


  def test_login_not_activated(self):
    '''Test login failed with non activated user'''
    inactivated_user_data = {
      'email': 'inactiveuser@example.com',
      'username': 'inactiveuser@example.com',
      'password': 'testpassword123'
    }

    inactive_user = User.objects.create(**inactivated_user_data)

    data = {
      'email': inactivated_user_data['email'],
      'password': inactivated_user_data['password']
    }

    response = self.client.post(self.login_url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertIn('message', response.data)
    self.assertEqual(response.data['message'], 'Invalid username or password.')

  def test_login_empty_fields(self):
    '''Test login failed with empty fields.'''
    data = {
      'email': '',
      'password': self.user_data['password']
    }

    response = self.client.post(self.login_url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    data = {
      'email': self.user_data['email'],
      'password': ''
    }

    response = self.client.post(self.login_url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



