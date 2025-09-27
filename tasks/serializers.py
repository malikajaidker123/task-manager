from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""
    owner = serializers.ReadOnlyField(source='owner.email')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']

    def create(self, validated_data):
        # ""
        # Create and return a new Task instance, given the validated data.
        # The owner is automatically set to the current user.
        # ""
        # The owner is set to the current user from the request context
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
