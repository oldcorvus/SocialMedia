
from rest_framework import serializers

from .models import Action, Contact


class ActionSerializer(serializers.ModelSerializer):
    """Serializer for the Action object"""

    class Meta:
        model = Action
        exclude = ('target_ct', 'target_id', 'created')
        read_only_fields = ('user','target' )

    def create(self, validated_data):
        """Create a new Action and return it"""
        return Action.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a Action,  and return it"""
        return super().update(instance, validated_data)

class ConatctSerializer(serializers.ModelSerializer):
    """Serializer for the contact object"""

    class Meta:
        model = Contact
        exclude = ( 'created',)
        read_only_fields = ( 'user_from', )

    def create(self, validated_data):
        """Create a new Action and return it"""
        return Action.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a Action,  and return it"""
        return super().update(instance, validated_data)
