from django.urls import path, include
from rest_framework import routers
from telegram_api.views import TaskViewSet, TelegramUserByUsername

router = routers.DefaultRouter()
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('telegram_users/', TelegramUserByUsername.as_view(), name='telegram-user-by-username'),
]

app_name = "task"
