from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = 'testing@tester.com'
        password = 'Testing123!'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normalized"""
        email = 'test@TESTINGPERSON.COM'
        user = get_user_model().objects.create_user(email, 'Testing1234')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test that user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Testing123')

    def test_super_user_is_created(self):
        """Test that new superuser has correct flags"""
        user = get_user_model().objects.create_superuser(
            'test@testing.com',
            'testing123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
