from django.test import TestCase, Client
from core_storage.models import Catalog
from tests.constants import DATA_CATALOG,  PURCHASE_DATA
from http import HTTPStatus


class StorageURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.guest_client.post("/catalog/", data=DATA_CATALOG[0])

    def test_catalog_page(self):
        response = self.guest_client.get('/catalog/')
        self.assertEqual(response.status_code, 200)


class ArrivalURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.cat_obj = self.guest_client.post("/catalog/", data=DATA_CATALOG[0])
        PURCHASE_DATA["catalog_name"] = self.cat_obj.data.get("id")
        self.purchase_obj = self.guest_client.post("/purchase/", data=PURCHASE_DATA)

    def test_arrival_page(self):
        """Проверка возвращаемого ответа 201 при создании записи в InStock"""
        data = {}
        data["name"] = self.purchase_obj.data.get("id")
        data["volume"] = self.purchase_obj.data.get("volume")
        response = self.guest_client.post('/arrival/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED, "Статус ответа не соответсвует")
