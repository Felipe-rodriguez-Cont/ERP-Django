from django.test import TestCase
from .models import Task
# Create your tests here.

#instalar pytest

class TaskModelTestCase(TestCase):
    def test_task_creation(self):
        task = Task.objects.create(
            name='Test task',
            description='This is a test task.'
        )
        self.assertEqual(task.name, 'Test task')
        self.assertEqual(task.description, 'This is a test task.')
        
# se debe ejecutar con python manage.py test