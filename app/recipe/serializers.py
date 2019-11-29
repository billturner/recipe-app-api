from rest_framework import serializers

from core.models import Ingredient, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for our tag model"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the ingredient model"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
