from pprint import pprint
from tests.constants import DATA_CATALOG, CATEGORIES, PURCHASE_DATA, TEN_ITERATIONS
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
        PURCHASE_DATA["catalog_name"] = cls.catalog_object.id
        for i in range(TEN_ITERATIONS):
            cls.my_client.post(
                "/purchase/",
                data=PURCHASE_DATA,
                content_type='application/json'
            )

    def test_create_purchase(self):
        """Проверяем создание записи в Purchase"""
        get_obj = Purchase.objects.filter(catalog_name=self.catalog_object.id).first()
        expected = "wax_1"
        self.assertEqual(expected, get_obj.catalog_name.name)

    def test_list_purchase_viewset(self):
        """Вывод всех записей."""
        response = self.my_client.get("/purchase/")
        expected = TEN_ITERATIONS
        total_row = len(response.data)
        self.assertEqual(total_row, expected, "Выводимое количество покупок, не соответствует")

    def test_retrieve_purchase(self):
        """Проверяем выдается ли запись по индексу"""
        purchase_response = self.my_client.get("/purchase/")
        purchase_id = purchase_response.data[-1].get('id')
        purchase_id_response = self.my_client.get(f"/purchase/{purchase_id}/")
        expected = self.catalog_object.name
        catalog_name = purchase_id_response.data.get('catalog_name')
        get_read_catalog_name = Catalog.objects.get(id=catalog_name).name
        self.assertEqual(expected, get_read_catalog_name, "Не выводит элемент по индексу")

    def test_create_arrivalwait(self):
        """Проверяем создание записи в ArrivalAwait"""
        arival_obj = ArrivalWait.objects.get(catalog_name=self.catalog_object.id)
        expected = "wax_1"
        self.assertEqual(expected, arival_obj.catalog_name.name, "Запись в arrivalwait не создана")

    def test_calculate_arrivalwait(self):
        """Проверка суммирования одинаковых заказов в ArrivalAwait"""
        arival_quantity = ArrivalWait.objects.get(catalog_name=self.catalog_object.id).quantity
        expected = TEN_ITERATIONS
        self.assertEqual(expected, arival_quantity, "Не правильно суммируются заказы")
