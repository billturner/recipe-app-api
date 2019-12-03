from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def sample_user(email='test@testing.com', password='Testing123!'):
    """Creating a sample user for our tests"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and eggs',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        """Test that image is saved in correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
