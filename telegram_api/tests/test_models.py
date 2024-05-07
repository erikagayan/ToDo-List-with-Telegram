from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from telegram_api.models import Task

User = get_user_model()


class TaskModelTest(TestCase):

    def setUp(self):
        # User for tests
        self.user = User.objects.create_user(username="testuser", password="password")

        # Test task
        self.task = Task.objects.create(
            telegram_id=123456789,
            title="Test Task",
            description="This is a test task.",
            due_date=date.today(),
            completed=False
        )

    def test_task_creation(self):
        """Create task"""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "This is a test task.")
        self.assertEqual(self.task.due_date, date.today())
        self.assertFalse(self.task.completed)
        self.assertEqual(str(self.task), "Test Task")

    def test_task_completion(self):
        """Update task"""
        self.task.completed = True
        self.task.save()
        self.assertTrue(self.task.completed)
