from django.test import TestCase, Client
from core_storage.models import Catalog


class StorageURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()
        self.catalog_row = Catalog.objects.create(
            name="wosk"
        )

    def test_catalog_page(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
