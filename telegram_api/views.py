from django.shortcuts import render
from rest_framework import mixins, viewsets, generics
from telegram_api.models import Task, TelegramUser
from telegram_api.serializers import TaskSerializer, TelegramUserSerializer


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


class TelegramUserByUsername(generics.RetrieveAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    lookup_field = 'username'