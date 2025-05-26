from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone # Needed for dates
from .models import Project, Task
from .forms import ProjectForm, TaskForm # Added TaskForm

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

class ProjectEditingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        self.project1 = Project.objects.create(name='Original Project Name', description='Original Description', user=self.user1)
        
        self.edit_url = reverse('tasks:project_edit', kwargs={'pk': self.project1.pk})
        self.project_detail_url = reverse('tasks:project_detail', kwargs={'pk': self.project1.pk})
        self.login_url = reverse('login') 

    def test_project_edit_view_get_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/project_form.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertEqual(response.context['form'].instance, self.project1)
        self.assertEqual(response.context['page_title'], 'Edit Project')

    def test_project_edit_view_post_owner_valid(self):
        self.client.login(username='user1', password='password123')
        updated_data = {
            'name': 'Updated Project Name',
            'description': 'Updated Description'
        }
        response = self.client.post(self.edit_url, data=updated_data)
        self.assertRedirects(response, self.project_detail_url)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, updated_data['name'])
        self.assertEqual(self.project1.description, updated_data['description'])

    def test_project_edit_view_post_owner_invalid(self):
        self.client.login(username='user1', password='password123')
        invalid_data = {
            'name': '',  # Name is required
            'description': 'Description for invalid form'
        }
        response = self.client.post(self.edit_url, data=invalid_data)
        self.assertEqual(response.status_code, 200) # Should re-render the form
        self.assertFormError(response, 'form', 'name', 'This field is required.')
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, 'Original Project Name') # Name should not change

    def test_project_edit_view_get_not_owner(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 404) # View uses get_object_or_404 with user filter

    def test_project_edit_view_post_not_owner(self):
        self.client.login(username='user2', password='password123')
        updated_data = {
            'name': 'Attempted Update by User2',
            'description': 'Should not work'
        }
        response = self.client.post(self.edit_url, data=updated_data)
        self.assertEqual(response.status_code, 404)
        self.project1.refresh_from_db()
        self.assertEqual(self.project1.name, 'Original Project Name') # Name should not change

    def test_project_edit_view_get_unauthenticated(self):
        response = self.client.get(self.edit_url)
        expected_redirect_url = f"{self.login_url}?next={self.edit_url}"
        self.assertRedirects(response, expected_redirect_url)

class TaskEditingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        self.project1 = Project.objects.create(name='Project 1 for Task Editing', user=self.user1)
        self.task1 = Task.objects.create(
            description='Original Task Description', 
            project=self.project1,
            status='todo',
            due_date=timezone.now().date() + timezone.timedelta(days=7)
        )
        
        self.edit_url = reverse('tasks:task_edit', kwargs={'pk': self.task1.pk})
        self.project_detail_url = reverse('tasks:project_detail', kwargs={'pk': self.project1.pk})
        self.project_list_url = reverse('tasks:project_list')
        self.login_url = reverse('login')

    def test_task_edit_view_get_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertIsInstance(response.context['form'], TaskForm)
        self.assertEqual(response.context['form'].instance, self.task1)
        self.assertEqual(response.context['page_title'], 'Edit Task')
        self.assertEqual(response.context['project'], self.project1) # Check project context

    def test_task_edit_view_post_owner_valid(self):
        self.client.login(username='user1', password='password123')
        valid_due_date = (timezone.now().date() + timezone.timedelta(days=10)).strftime('%Y-%m-%d')
        updated_data = {
            'description': 'Updated Task Description',
            'status': 'doing',
            'due_date': valid_due_date 
        }
        response = self.client.post(self.edit_url, data=updated_data)
        self.assertRedirects(response, self.project_detail_url)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.description, updated_data['description'])
        self.assertEqual(self.task1.status, updated_data['status'])
        self.assertEqual(self.task1.due_date.strftime('%Y-%m-%d'), valid_due_date)

    def test_task_edit_view_post_owner_invalid(self):
        self.client.login(username='user1', password='password123')
        invalid_data = {
            'description': '',  # Description is required
            'status': 'done' 
        }
        response = self.client.post(self.edit_url, data=invalid_data)
        self.assertEqual(response.status_code, 200) # Should re-render the form
        self.assertFormError(response, 'form', 'description', 'This field is required.')
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.description, 'Original Task Description') # Description should not change

    def test_task_edit_view_get_not_owner(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.edit_url)
        # View logic: if project.user != request.user: return redirect('tasks:project_list')
        self.assertRedirects(response, self.project_list_url)

    def test_task_edit_view_post_not_owner(self):
        self.client.login(username='user2', password='password123')
        updated_data = {
            'description': 'Attempted Update by User2',
            'status': 'done'
        }
        response = self.client.post(self.edit_url, data=updated_data)
        # View logic: if project.user != request.user: return redirect('tasks:project_list')
        self.assertRedirects(response, self.project_list_url)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.description, 'Original Task Description') # Description should not change

    def test_task_edit_view_get_unauthenticated(self):
        response = self.client.get(self.edit_url)
        expected_redirect_url = f"{self.login_url}?next={self.edit_url}"
        self.assertRedirects(response, expected_redirect_url)
