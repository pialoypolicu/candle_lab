from django.test import TestCase, Client
from core_storage.models import Catalog
from tests.constants import DATA_CATALOG


class StorageURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.guest_client.post("/catalog/", data=DATA_CATALOG[0])

    def test_catalog_page(self):
        response = self.guest_client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
