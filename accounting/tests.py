from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Transaction, Category # Assuming Category might be needed, or can be null

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
