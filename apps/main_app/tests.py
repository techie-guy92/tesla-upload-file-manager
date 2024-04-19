from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounting.models import CustomUser

class FileViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_delete_file(self):
        response = self.client.delete(reverse('delete-file', kwargs={'file_id': 1}))
        self.assertEqual(response.status_code, 404)  # Assuming file_id 1 does not exist

    def test_download_file(self):
        response = self.client.get(reverse('download-file', kwargs={'file_id': 1}))
        self.assertEqual(response.status_code, 404)  # Assuming file_id 1 does not exist

    def test_permission_denied(self):
        self.client.logout()
        response = self.client.delete(reverse('delete-file', kwargs={'file_id': 1}))
        self.assertEqual(response.status_code, 403)  # Expecting permission denied

        response = self.client.get(reverse('download-file', kwargs={'file_id': 1}))
        self.assertEqual(response.status_code, 403)  # Expecting permission denied
