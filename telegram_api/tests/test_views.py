from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.utils import timezone
from datetime import timedelta
from telegram_api.models import Task


class TaskViewSetTest(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create task
        self.task = Task.objects.create(
            telegram_id=123456789,
            title='Initial Task',
            description='A test task.',
            due_date=timezone.now().date(),
            completed=False
        )

        self.list_create_url = reverse('task:task-list')

        self.detail_url = reverse('task:task-detail', kwargs={'pk': self.task.pk})

    def test_get_all_tasks(self):
        """List of tasks"""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_task(self):
        """One task"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Initial Task')

    def test_create_task(self):
        """Create a new task"""
        data = {
            'telegram_id': 987654321,
            'title': 'New Task',
            'description': 'Another test task.',
            'due_date': (timezone.now() + timedelta(days=1)).date(),
            'completed': False
        }
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_update_task(self):
        """Update task"""
        data = {
            'title': 'Updated Task',
            'description': 'Updated description.',
            'completed': True
        }
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.title, 'Updated Task')
        self.assertTrue(updated_task.completed)

    def test_delete_task(self):
        """Delete task"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
