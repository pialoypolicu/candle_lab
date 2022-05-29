import time
from pprint import pprint
from tests.constants import DATA_CATALOG, CATEGORIES, PURCHASE_DATA, TEN_ITERATIONS
from django.test import TestCase
from django.test.client import Client
from core_storage.models import Catalog, Purchase
from http import HTTPStatus


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
        """Проверяем создание записи, с частичными совпадениями"""
        total = Catalog.objects.filter(name="wax_2").count()
        expected = total >= 3
        self.assertTrue(expected, "Не была создана отличная запись")

    def test_return_catalog_items(self):
        """Проверяем, что выводим все записи из каталога
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
        purchase_id_data = purchase_id_response.data
        comment = purchase_id_data.get("comment")
        get_read_catalog_name = Catalog.objects.get(id=self.catalog_object.id).name
        expected = self.catalog_object.name
        self.assertEqual(expected, get_read_catalog_name, "Не выводит элемент по индексу")
        expected_comment = "Very good candles"
        self.assertEqual(expected_comment, comment, "Комментарий  не  соответствует")

    def test_put_purchase(self):
        """Проверим будет ли выполнено изменение на методе PUT"""
        purchase_id = self.my_client.get("/purchase/").data[-1].get('id')
        data = {"quantity": 3}
        purchase_id_response = self.my_client.put(f"/purchase/{purchase_id}/", data=data)
        expected = HTTPStatus.METHOD_NOT_ALLOWED
        self.assertEqual(expected, purchase_id_response.status_code, "Статус ответа не совпаадает с ожидаемым")


class ArrivalTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.my_client = Client()
        cls.cat_obj = cls.my_client.post("/catalog/", data=DATA_CATALOG[0])
        PURCHASE_DATA["catalog_name"] = cls.cat_obj.data.get("id")
        cls.purchase_obj = cls.my_client.post("/purchase/", data=PURCHASE_DATA)
        cls.purchase_obj_id = cls.purchase_obj.data.get("id")
        response_purchase = cls.my_client.get(f"/purchase/{cls.purchase_obj_id}/")
        cls.data_to_instock = {
            "name": response_purchase.data["catalog_name"],
            "volume": response_purchase.data["volume"]
        }
        cls.my_client.post("/arrival/", data=cls.data_to_instock)

    def test_create_object_in_stock(self):
        """Проверяем создание записи в таблице InStock"""
        instock_object = self.my_client.get("/instock/")
        for field, expected_value in self.data_to_instock.items():
            with self.subTest(field=field):
                self.assertEqual(
                    instock_object.data[0].get(field), expected_value, "Запись в таблице instock не создана")

    def test_unique_object_instock(self):
        """Проверка, что вторая запись с таким же названием в InStoc не создается"""
        response = self.my_client.get("/instock/")
        expected_objects = len(response.data)
        self.my_client.post("/arrival/", data=self.data_to_instock)
        total_objects_instock = len(self.my_client.get("/instock/").data)
        self.assertEqual(total_objects_instock, expected_objects, "создана не уникальная запись в instock")

    def test_update_object_instock(self):
        """Проверка изменения сушествующего объекта"""
        self.my_client.post("/arrival/", data=self.data_to_instock)
        expected_objects = 60
        total_object_volume = self.my_client.get("/instock/").data[0]["volume"]
        self.assertEqual(total_object_volume, expected_objects, "Запись в InStock не обновлена")
