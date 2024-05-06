from rest_framework import serializers
from telegram_api.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'telegram_id', 'title', 'description', 'due_date', 'completed']

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task

