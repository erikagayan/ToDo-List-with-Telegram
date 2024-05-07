from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from rest_framework.exceptions import ValidationError
from telegram_api.models import Task
from telegram_api.serializers import TaskSerializer

User = get_user_model()


class TaskSerializerTest(TestCase):
    def setUp(self):
        # User for tests
        self.user = User.objects.create_user(username='testuser', password='password')

        # Test task
        self.task = Task.objects.create(
            telegram_id=123456789,
            title='Test Task',
            description='This is a test task.',
            due_date=date.today(),
            completed=False
        )

    def test_serializer_with_empty_data(self):
        """Empty data"""
        data = {}
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['telegram_id', 'title', 'due_date']))

    def test_serializer_with_valid_data(self):
        """Valid data"""
        data = {
            'telegram_id': 987654321,
            'title': 'Another Test Task',
            'description': '',
            'due_date': date.today(),
            'completed': True
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        created_task = serializer.save()
        self.assertEqual(created_task.title, 'Another Test Task')
        self.assertEqual(created_task.completed, True)
        self.assertEqual(Task.objects.count(), 2)

    def test_serializer_output(self):
        """Serializator output"""
        serializer = TaskSerializer(instance=self.task)
        self.assertEqual(serializer.data, {
            'id': self.task.id,
            'telegram_id': 123456789,
            'title': 'Test Task',
            'description': 'This is a test task.',
            'due_date': self.task.due_date.isoformat(),
            'completed': False
        })
