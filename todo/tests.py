from django.test import TestCase
from .models import Todo
from django.urls import reverse

class TodoModelTest(TestCase):

    def setUp(self):
        self.todo = Todo.objects.create(
            title='Test Todo',
            description='This is a test todo',
            completed=False
        )

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, 'Test Todo')
        self.assertEqual(self.todo.description, 'This is a test todo')
        self.assertFalse(self.todo.completed)

class TodoViewsTest(TestCase):

    def setUp(self):
        self.todo = Todo.objects.create(
            title='Test Todo',
            description='This is a test todo',
            completed=False
        )

    def test_todo_list_view(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Todo')
        self.assertTemplateUsed(response, 'todo/index.html')

    def test_todo_detail_view(self):
        response = self.client.get(reverse('todo_detail', args=[self.todo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Todo')
        self.assertTemplateUsed(response, 'todo/todo_detail.html')

    def test_todo_create_view(self):
        response = self.client.post(reverse('todo_create'), {
            'title': 'New Todo',
            'description': 'This is a new todo',
            'completed': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.last().title, 'New Todo')

    def test_todo_update_view(self):
        response = self.client.post(reverse('todo_edit', args=[self.todo.id]), {
            'title': 'Updated Todo',
            'description': 'This is an updated todo',
            'completed': True
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')
        self.assertTrue(self.todo.completed)

    def test_todo_delete_view(self):
        response = self.client.post(reverse('todo_delete', args=[self.todo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())
