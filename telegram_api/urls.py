from django.urls import path, include
from rest_framework import routers
from telegram_api.views import TaskViewSet

router = routers.DefaultRouter()
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "task"
