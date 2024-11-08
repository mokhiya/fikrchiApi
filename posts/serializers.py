from rest_framework import serializers
from .models import PostModel


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        # This method saves the note to the user making the request
        return PostModel.objects.create(**validated_data)
