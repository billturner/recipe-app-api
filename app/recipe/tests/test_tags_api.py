from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required"""

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@testing.com',
            'Tesing123!'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test we're retrieving a list of tags"""
        Tag.objects.create(user=self.user, name='vegan')
        Tag.objects.create(user=self.user, name='dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test we only return tags for provided user"""
        user2 = get_user_model().objects.create_user(
            'other@testing.com',
            'AnotherPass123!'
        )
        Tag.objects.create(user=user2, name='fruit')
        tag = Tag.objects.create(user=self.user, name='appetizers')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tags_successful(self):
        """Testing creation of tags"""
        payload = {'name': 'test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_invalid_tag(self):
        """Test creating an invalid tag fails"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_recipes(self):
        """Return tags assigned to recipes"""
        tag1 = Tag.objects.create(user=self.user, name='vegan')
        tag2 = Tag.objects.create(user=self.user, name='vegetarian')
        recipe = Recipe.objects.create(
            user=self.user,
            title='Something tasty',
            time_minutes=10,
            price=5.00
        )
        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assigned_unique(self):
        """Test filtering tag by assigned are unique"""
        tag1 = Tag.objects.create(user=self.user, name='vegan')
        Tag.objects.create(user=self.user, name='vegetarian')
        recipe1 = Recipe.objects.create(
            user=self.user,
            title='Something tasty',
            time_minutes=10,
            price=5.00
        )
        recipe1.tags.add(tag1)
        recipe2 = Recipe.objects.create(
            user=self.user,
            title='Something Else',
            time_minutes=20,
            price=50.00
        )
        recipe2.tags.add(tag1)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
