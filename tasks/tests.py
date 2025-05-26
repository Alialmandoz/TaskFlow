from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project, Task

# Create your tests here.
class TaskDeletionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        self.project1 = Project.objects.create(name='Project 1', user=self.user1)
        self.task1 = Task.objects.create(description='Task 1 for Project 1', project=self.project1)
        
        self.delete_url = reverse('tasks:task_delete', kwargs={'task_pk': self.task1.pk})
        self.project_detail_url = reverse('tasks:project_detail', kwargs={'pk': self.project1.pk})
        self.login_url = reverse('login') # Assuming your login URL is named 'login'

    def test_delete_task_authenticated_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.project_detail_url)
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_delete_task_unauthenticated(self):
        response = self.client.post(self.delete_url)
        # Check if it redirects to the login page, then to the intended page or a similar pattern
        expected_redirect_url = f"{self.login_url}?next={self.delete_url}"
        self.assertRedirects(response, expected_redirect_url, fetch_redirect_response=False) # Check only the initial redirect
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())

    def test_delete_task_not_owner(self):
        # Log in as user2 who does not own the project/task
        self.client.login(username='user2', password='password123')
        response = self.client.post(self.delete_url)
        
        # The view redirects to 'tasks:project_list' if task.project.user != request.user
        # This is not a 404 based on the current view logic.
        # If the view logic was get_object_or_404(Task, pk=task_pk, project__user=request.user) it would be 404.
        # Current logic: task = get_object_or_404(Task, pk=task_pk) then if task.project.user != request.user: return redirect('tasks:project_list')
        self.assertRedirects(response, reverse('tasks:project_list'))
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())

    def test_delete_task_get_request_not_allowed(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 405) # Method Not Allowed
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())
