
from unittest.mock import call
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Article, Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the category object"""

    class Meta:
        model = Category
        fields = ('title', 'cover', 'status', 'description', 
        'parent' )

    def create(self, validated_data):
        """Create a new category and return it"""
        return Category.objects.create(**validated_data )

    def update(self, instance, validated_data):
        """Update a category,  and return it"""
        return super().update(instance, validated_data)
         
        
        

class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the article object"""
    class Meta:
        model = Article
        exclude = ('created', 'updated','author','users_like')
        read_only_fields = ('author',)

    def create(self, validated_data):
        """Create a new article  and return it"""
        category_data = validated_data.pop('category')
        article = Article.objects.create(**validated_data)
        article.category.add(*category_data)
        
        return article

    def update(self, instance, validated_data):
        """Update a article,  and return it"""
        return super().update(instance, validated_data)
         
