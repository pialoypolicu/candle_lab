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

class PurchaseURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.response = self.guest_client.post("/purchase/", data=PURCHASE_DATA)

    def test_404_error(self):
        """Проверка 404 ошибки если запись не создана в Catalog"""
        self.assertEqual(HTTPStatus.NOT_FOUND, self.response.status_code, "Ответ != 404")


class ArrivalURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.cat_obj = self.guest_client.post("/catalog/", data=DATA_CATALOG[0])
        PURCHASE_DATA["catalog_name"] = self.cat_obj.data.get("id")
        self.purchase_response = self.guest_client.post("/purchase/", data=PURCHASE_DATA)
        self.purchase_data = self.purchase_response.data

    def test_arrival_page(self):
        """Проверка возвращаемого ответа 201 при создании записи в InStock"""
        data = {
            "name": self.purchase_data["name"],
            "volume": self.purchase_data["volume"],
            "quantity": self.purchase_data["quantity"],
            "company": self.purchase_data["company"],
        }
        response = self.guest_client.post('/arrival/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED, "Статус ответа не соответствует")


class InStockURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
#         self.cat_obj = self.guest_client.post("/catalog/", data=DATA_CATALOG[0])
#         PURCHASE_DATA["catalog_name"] = self.cat_obj.data.get("id")
#         self.purchase_obj = self.guest_client.post("/purchase/", data=PURCHASE_DATA)
#         data = {}
#         data["name"] = self.purchase_obj.data.get("id")
#         data["volume"] = self.purchase_obj.data.get("volume")
#         self.guest_client.post('/arrival/', data=data)
        self.response = self.guest_client.get("/instock/")
#
    def test_arrival_page(self):
        """Проверка возвращаемого ответа 200 при запросе списка InStock"""
        expected = HTTPStatus.OK
        self.assertEqual(self.response.status_code, expected, "Статус ответа не соответствует")


# class ProductionURLTests(TestCase):
#     def setUp(self):
#         self.guest_client = Client()
#         self.response = self.guest_client.put("/production/")
#
#
#     def test_smoke(self):
#         """Проверка smoke test production"""
#         expected = HTTPStatus.OK
#         print(dir(self.response))
#         print("content", self.response.content)
#         print("context", self.response.context)
#         self.assertEqual(self.response.status_code, expected, "Статус ответа не соответствует")
