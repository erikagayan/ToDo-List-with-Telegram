from django.shortcuts import render
from rest_framework import mixins, viewsets
from telegram_api.models import Task
from telegram_api.serializers import TaskSerializer


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
