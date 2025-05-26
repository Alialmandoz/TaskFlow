from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Transaction, Category
from tasks.models import Project # For creating a project to link to a transaction
from .forms import TransactionForm # For checking form instance and field scoping

# Create your tests here.
class TransactionDeletionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # Optional: Create a category if your Transaction model requires it or for more thorough testing
        # self.category1 = Category.objects.create(name='Test Category', user=self.user1)

        self.transaction1 = Transaction.objects.create(
            description='Test Expense 1',
            amount=100.00,
            user=self.user1,
            transaction_date=timezone.now().date()
            # category=self.category1 # Assign if category is created and required
        )
        
        self.delete_url = reverse('accounting:transaction_delete', kwargs={'transaction_pk': self.transaction1.pk})
        self.transaction_list_url = reverse('accounting:transaction_list')
        self.login_url = reverse('login') # Assuming your login URL is named 'login'

    def test_delete_transaction_authenticated_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.transaction_list_url)
        self.assertFalse(Transaction.objects.filter(pk=self.transaction1.pk).exists())

    def test_delete_transaction_unauthenticated(self):
        response = self.client.post(self.delete_url)
        expected_redirect_url = f"{self.login_url}?next={self.delete_url}"
        self.assertRedirects(response, expected_redirect_url, fetch_redirect_response=False)
        self.assertTrue(Transaction.objects.filter(pk=self.transaction1.pk).exists())

    def test_delete_transaction_not_owner(self):
        self.client.login(username='user2', password='password123')
        response = self.client.post(self.delete_url)
        # Based on the view logic: transaction = get_object_or_404(Transaction, pk=transaction_pk)
        # then if transaction.user != request.user: return redirect('accounting:transaction_list')
        # So, it's a redirect, not a 404, if the user is simply not the owner.
        # A 404 would occur if the view used get_object_or_404(Transaction, pk=transaction_pk, user=request.user)
        self.assertRedirects(response, self.transaction_list_url)
        self.assertTrue(Transaction.objects.filter(pk=self.transaction1.pk).exists())

    def test_delete_transaction_get_request_not_allowed(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 405) # Method Not Allowed
        self.assertTrue(Transaction.objects.filter(pk=self.transaction1.pk).exists())

class TransactionEditingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        self.category_user1 = Category.objects.create(name='Groceries', user=self.user1)
        self.category_user1_alt = Category.objects.create(name='Utilities', user=self.user1)
        self.category_user2 = Category.objects.create(name='Entertainment', user=self.user2)
        
        self.project_user1 = Project.objects.create(name='Household Chores', user=self.user1)
        self.project_user1_alt = Project.objects.create(name='Work Project', user=self.user1)
        self.project_user2 = Project.objects.create(name='User2 Project', user=self.user2)

        self.transaction1 = Transaction.objects.create(
            description='Original Transaction Desc',
            amount=50.00,
            user=self.user1,
            transaction_date=timezone.now().date(),
            category=self.category_user1,
            project=self.project_user1
        )
        
        self.edit_url = reverse('accounting:transaction_edit', kwargs={'pk': self.transaction1.pk})
        self.transaction_list_url = reverse('accounting:transaction_list')
        self.login_url = reverse('login')

    def test_transaction_edit_view_get_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounting/transaction_form.html')
        self.assertIsInstance(response.context['form'], TransactionForm)
        self.assertEqual(response.context['form'].instance, self.transaction1)
        self.assertEqual(response.context['page_title'], 'Edit Transaction')
        
        # Check category and project queryset scoping
        form_in_context = response.context['form']
        self.assertQuerysetEqual(
            form_in_context.fields['category'].queryset.order_by('name'),
            Category.objects.filter(user=self.user1).order_by('name'),
            transform=lambda x: x
        )
        self.assertQuerysetEqual(
            form_in_context.fields['project'].queryset.order_by('name'),
            Project.objects.filter(user=self.user1).order_by('name'),
            transform=lambda x: x
        )

    def test_transaction_edit_view_post_owner_valid(self):
        self.client.login(username='user1', password='password123')
        updated_data = {
            'description': 'Updated Transaction Description',
            'amount': 120.50,
            'transaction_date': (timezone.now() - timezone.timedelta(days=1)).strftime('%Y-%m-%d'),
            'category': self.category_user1_alt.pk,
            'project': self.project_user1_alt.pk,
            'notes': 'Updated notes here',
            'type': 'expense' # Type field is usually part of the form
        }
        response = self.client.post(self.edit_url, data=updated_data)
        self.assertRedirects(response, self.transaction_list_url)
        self.transaction1.refresh_from_db()
        self.assertEqual(self.transaction1.description, updated_data['description'])
        self.assertEqual(float(self.transaction1.amount), updated_data['amount'])
        self.assertEqual(self.transaction1.transaction_date.strftime('%Y-%m-%d'), updated_data['transaction_date'])
        self.assertEqual(self.transaction1.category, self.category_user1_alt)
        self.assertEqual(self.transaction1.project, self.project_user1_alt)
        self.assertEqual(self.transaction1.notes, updated_data['notes'])

    def test_transaction_edit_view_post_owner_invalid(self):
        self.client.login(username='user1', password='password123')
        invalid_data = {
            'description': 'Test Invalid',
            'amount': 'not-a-number', # Invalid amount
            'transaction_date': timezone.now().date().strftime('%Y-%m-%d'),
            'category': self.category_user1.pk,
            'type': 'expense'
        }
        response = self.client.post(self.edit_url, data=invalid_data)
        self.assertEqual(response.status_code, 200) # Should re-render the form
        self.assertFormError(response, 'form', 'amount', 'Enter a number.')
        self.transaction1.refresh_from_db()
        self.assertEqual(self.transaction1.description, 'Original Transaction Desc') # Description should not change

    def test_transaction_edit_view_get_not_owner(self):
        self.client.login(username='user2', password='password123')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 404)

    def test_transaction_edit_view_post_not_owner(self):
        self.client.login(username='user2', password='password123')
        updated_data = {
            'description': 'Attempted Update by User2',
            'amount': 200.00,
            'transaction_date': timezone.now().date().strftime('%Y-%m-%d'),
            'type': 'expense'
        }
        response = self.client.post(self.edit_url, data=updated_data)
        self.assertEqual(response.status_code, 404)
        self.transaction1.refresh_from_db()
        self.assertEqual(self.transaction1.description, 'Original Transaction Desc')

    def test_transaction_edit_view_get_unauthenticated(self):
        response = self.client.get(self.edit_url)
        expected_redirect_url = f"{self.login_url}?next={self.edit_url}"
        self.assertRedirects(response, expected_redirect_url)
