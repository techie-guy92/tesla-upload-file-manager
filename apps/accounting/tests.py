from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class ViewsTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_register_user_view(self):
        response = self.client.post(reverse('register_user'), self.user_data)
        self.assertEqual(response.status_code, 200)  # Check if registration is successful

    def test_verify_email_view(self):
        # Assuming you have stored the activation code in the session
        activation_code = 'your_activation_code_here'
        self.client.session['activation_code'] = activation_code
        response = self.client.get(reverse('verify-email', kwargs={'activation_code': activation_code}))
        self.assertEqual(response.status_code, 200)  # Check if email verification is successful

    def test_login_user_view(self):
        response = self.client.post(reverse('login'), self.user_data)
        self.assertEqual(response.status_code, 200)  # Check if login is successful

    def test_logout_user_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)  # Check if logout is successful

    def test_change_password_view(self):
        activation_code = 'your_activation_code_here'
        self.client.session['activation_code'] = activation_code
        new_password_data = {
            'password': 'newpassword',
            're_password': 'newpassword',
        }
        response = self.client.post(reverse('change-pass', kwargs={'activation_code': activation_code}), new_password_data)
        self.assertEqual(response.status_code, 200)  # Check if password change is successful
