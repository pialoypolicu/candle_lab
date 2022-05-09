from pprint import pprint
from tests.constants import DATA_CATALOG, CATEGORIES
from django.db import IntegrityError
from django.test import TestCase
from django.test.client import Client
from core_storage.models import Catalog, Purchase, ArrivalWait


class CatalogViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.my_client = Client()
        for data in DATA_CATALOG:
            cls.my_client.post("/catalog/", data=data)

    def test_unique_catalog(self):
        """Проверка на уникальность при создании записи"""
        total = Catalog.objects.filter(name="wax_1").count()
        expected = 1
        self.assertEqual(expected, total, "Был создан дубль")


    def test_create_row_catalog(self):
        """Прроверяем создание записи, с частичными совпадениями"""
        total = Catalog.objects.filter(name="wax_2").count()
        expected = total >= 3
        self.assertTrue(expected, "Не была создана отличная запись")

    def test_return_catalog_items(self):
        """Проверям, что выводим все записи из каталога
           data_catalog в данном списке, одна запись не валидна
        """
        response = self.my_client.get("/catalog/")
        total = len(response.data)
        expected_rows = len(DATA_CATALOG) - 1
        self.assertEqual(expected_rows, total, " Не верное возвращаемое количество записей")

    def test_catalog_category(self):
        """Проверяем, что  категория в объекте корректная"""
        response = self.my_client.get("/catalog/")
        data = response.data
        for idx in range(len(data)):
            category = data[idx]["category"]
            with self.subTest(field="try_test"):
                self.assertIn(category, CATEGORIES, "Категория не соответствует")


class CreatePurchaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.my_client = Client()
        cls.my_client.post("/catalog/", data=DATA_CATALOG[0])
        cls.catalog_object = Catalog.objects.get(name="wax_1")
        data = {
            "catalog_name_id": cls.catalog_object.id,
            "date_purchase": "2022-04-01",
            "quantity": 1,
            "weight": 30,
            "price": 1000,
        }
        cls.my_client.post(
            "/add-product/",
            data=data,
            content_type='application/json'
        )

    def test_create_purchase(self):
        """Проверяем создание записи в Purchase"""
        get_obj = Purchase.objects.get(catalog_name=self.catalog_object.id)
        expected = "wax_1"
        self.assertEqual(expected, get_obj.catalog_name.name)

    def test_create_arrivalwait(self):
        """Проверяем создание записи в ArrivalAwait"""
        arival_obj = ArrivalWait.objects.get(catalog_name=self.catalog_object.id)
        expected = "wax_1"
        self.assertEqual(expected, arival_obj.catalog_name.name)
