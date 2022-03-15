
from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the comment object"""

    class Meta:
        model = Comment
        exclude = ('content_type', 'object_id', 'created')
        read_only_fields = ('author', 'is_reply', 'reply')

    def create(self, validated_data):
        """Create a new comment and return it"""
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a comment,  and return it"""
        return super().update(instance, validated_data)
