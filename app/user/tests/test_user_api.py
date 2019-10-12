from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test valid payload creates a user successfully"""
        payload = {
            'email': 'test@testing.com',
            'password': 'TestPassword1$',
            'name': 'Sample User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'test@testing.com',
            'password': 'TestPassword1$'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_restriction(self):
        """Test that the password is more than 5 characters"""
        payload = {
            'email': 'test@testing.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@testing.com',
            'password': 'TestPasswd2'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created with invalid payload"""
        create_user(
            email='test@testing.com',
            password='TestPasswd2'
        )
        payload = {
            'email': 'test@testing.com',
            'password': 'NotThePasswd1'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist"""
        payload = {
            'email': 'test@testing.com',
            'password': 'TestPasswd2'
        }

        # user not created
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_parameter(self):
        """Test that email and password are both required"""
        res = self.client.post(
            TOKEN_URL,
            {
                'email': 'testing@somewhere.org',
                'password': ''
            }
        )

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
