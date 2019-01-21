from django.test import TestCase
from django.urls import reverse


class IndexTests(TestCase):
    def setUp(self):
        url = reverse('index')
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEqual(self.response.status_code, 200)
