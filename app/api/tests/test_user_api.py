import email
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


LOGIN_URL = reverse('rest_login')
TOKEN_URL = reverse('token_verify')
REFRESH_TOKEN_URL = reverse('token_refresh')
USER_URL = reverse('rest_user_details')
REGISTER_URL = '/api/dj-rest-auth/registration/'


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@moel.com',
            'password1': 'moelcrow@gmail.com',
            'password2': 'moelcrow@gmail.com',
            'username': 'username',
            'phone_number': 12213,
        }
        res = self.client.post(
            REGISTER_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email='test@moel.com',
                                            username='username', phone_number=12213)
        self.assertTrue(user.check_password(payload['password1']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creatinga  user that already exists fails"""
        payload = {
            'email': 'test@moel.com',
            'password1': 'moelcrow@gmail.com',
            'password2': 'moelcrow@gmail.com',
            'username': 'Test username',
            'phone_number': 99,
        }
        create_user(email='test@moel.com', password='moelcrow@gmail.com',
                    username='Test username', phone_number=99)

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@moel.com',
            'password1': 'pw',
            'password2': 'pw',
            'userusername': 'Test username',
            'phone_number': 99, }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'moelcrow@gmail.com',
            'password1': 'moelcrow@gmail.com',
            'password2': 'moelcrow@gmail.com',
            'username': 'moel',
            'phone_number': 13,
        }
        res = self.client.post(REGISTER_URL, payload)
        self.assertIn('access_token', res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@moel.com', password='moelcrow@gmail.com',
                    username='Test username', phone_number=99)
        payload = {'email': 'test@moel.com', 'password': 'wrong'}
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(400, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(USER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(email='test@moel.com', password='moelcrow@gmail.com',
                    username='Test username', phone_number=99)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        res = self.client.get(USER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'pk': 1, 'email': 'test@moel.com', 'first_name': '', 'last_name': ''})

    def test_post_user_not_allowed(self):
        """Test that POST is not allowed on the user  url"""
        res = self.client.post(USER_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'email': 'moelcrow@gmail.com', 'password': 'newpassword123'}
        res = self.client.patch('/api/users/1/', payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
        
