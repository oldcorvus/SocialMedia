
from rest_framework import serializers

from .models import ImageBookmark

class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for the bookmark object"""

    class Meta:
        model = ImageBookmark
        exclude = ('users_like',)

    def create(self, validated_data):
        """Create a new Bookmark and return it"""
        return ImageBookmark.objects.create(**validated_data )

    def update(self, instance, validated_data):
        """Update a Bookmark,  and return it"""
        return super().update(instance, validated_data)
         
        
        
