from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='moel@crow.com',
            password='password123',
            phone_number = 200000,
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@crow.com',
            password='password123',
            username='Test user full name',
            phone_number = 203240,
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:account_customuser_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:account_customuser_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:account_customuser_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)