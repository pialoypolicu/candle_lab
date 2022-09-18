import json
import random
from http import HTTPStatus
from pprint import pprint

from django.test import TestCase
from django.test.client import Client

from core_storage.models import Catalog, Purchase
from tests.constants import (CATEGORIES, DATA_CATALOG, PURCHASE_DATA,
                             TEN_ITERATIONS)


class Client:
    my_client = Client()


class CatalogViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.my_client = Client.my_client
        for data in DATA_CATALOG:
            cls.my_client.post("/catalog/", data=data)
        cls.catalog_list = cls.my_client.get("/catalog/")
        cls.catalog_obj = random.choice(cls.catalog_list.data)


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
        total = len(self.catalog_list.data)
        expected_rows = len(DATA_CATALOG) - 1
        self.assertEqual(expected_rows, total, " Не верное возвращаемое количество записей")

    def test_retrieve_catalog_item(self):
        """
        Проверяем retrieve метод. Возвращение правильного объекта по id.
        """
        catalog_obj_id = self.catalog_obj.get("id")
        response = self.my_client.get(f"/catalog/{catalog_obj_id}/")
        self.assertEqual(catalog_obj_id, response.data['id'], "Вернулся не верный объект")

    def test_catalog_category(self):
        """Проверяем, что  категория в объекте корректная"""
        data = self.catalog_list.data
        for idx in range(len(data)):
            category = data[idx]["category"]
            with self.subTest(field="try_test"):
                self.assertIn(category, CATEGORIES, "Категория не соответствует")


class PurchaseTest(TestCase):
    my_client = Client.my_client

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.response_catalog = cls.my_client.post("/catalog/", data=DATA_CATALOG[0])
        for i in range(10):
            cls.my_client.post(
                "/purchase/",
                data=PURCHASE_DATA,
                content_type='application/json'
            )
        cls.purchases = cls.my_client.get("/purchase/")

    def test_create_purchase(self):
        """Проверяем создание записи в Purchase"""
        get_obj = Purchase.objects.get(id=self.purchases.data[0]["id"])
        expected = "wax_1"
        self.assertEqual(expected, get_obj.catalog_name.name)

    def test_list_purchase_viewset(self):
        """Вывод всех записей."""
        expected = TEN_ITERATIONS
        total_row = len(self.purchases.data)
        self.assertEqual(total_row, expected, "Выводимое количество покупок, не соответствует")

    def test_retrieve_purchase(self):
        """Проверяем выдается ли запись по индексу"""
        expected_name = self.response_catalog.data.get("name")
        purchase_id = random.choice(self.purchases.data).get('id')
        purchase_id_response = Client.my_client.get(f"/purchase/{purchase_id}/")
        purchase_id_data = purchase_id_response.data
        purchase_comment = purchase_id_data.get("comment")
        purchase_name = purchase_id_data.get("name")
        self.assertEqual(expected_name, purchase_name, "Не выводит элемент по индексу")

    def test_put_purchase(self):
        """Проверим будет ли выполнено изменение на методе PUT"""
        purchase_id = Client.my_client.get("/purchase/").data[-1].get('id')
        data = {"quantity": 3}
        purchase_id_response = Client.my_client.put(f"/purchase/{purchase_id}/", data=data)
        expected = HTTPStatus.METHOD_NOT_ALLOWED
        self.assertEqual(expected, purchase_id_response.status_code, "Статус ответа не совпаадает с ожидаемым")

    def test_raise_parse_error(self):
        PURCHASE_DATA["name"] = "wax_2"
        response = self.my_client.post(
            "/purchase/",
            data=PURCHASE_DATA,
            content_type='application/json'
        )
        expected_text_error = f'object - {PURCHASE_DATA["name"]} not exists'
        response_text = json.loads(response.content)["detail"]
        self.assertEqual(expected_text_error, response_text, "Текст ошибки не совпадает")


class ArrivalInstockTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cat_obj = Client.my_client.post("/catalog/", data=DATA_CATALOG[0])
        PURCHASE_DATA["catalog_name"] = cls.cat_obj.data.get("id")
        cls.purchase_obj = Client.my_client.post("/purchase/", data=PURCHASE_DATA)
        cls.purchase_obj_id = cls.purchase_obj.data.get("id")
        response_purchase = Client.my_client.get(f"/purchase/{cls.purchase_obj_id}/")
        cls.data_to_instock = {
            "name": response_purchase.data["catalog_name"],
            "volume": response_purchase.data["volume"],
            "quantity": 2,
            "availability": True
        }
        cls.arrival_response = Client.my_client.post(
            "/arrival/",
            data=cls.data_to_instock,
            content_type="application/json"
        )
        cls.base_expected_volume = cls.data_to_instock["volume"] * cls.data_to_instock["quantity"]
        cls.instock_objects = Client.my_client.get("/instock/")

    def test_create_object_instock(self):
        """Проверяем создание записи в таблице InStock"""
        self.assertEqual(self.data_to_instock['name'], self.instock_objects.data[0]['name'], "Запись в таблице instock не создана")

    def test_volume_field(self):
        self.assertEqual(self.base_expected_volume, self.instock_objects.data[0]['volume'], "Не верно quantity")

    def test_unique_object_instock(self):
        """Проверка, что вторая запись с таким же названием в InStock не создается"""
        expected_objects = len(self.instock_objects.data)
        Client.my_client.post("/arrival/", data=self.data_to_instock, content_type="application/json")
        total_objects_instock = len(Client.my_client.get("/instock/").data)
        self.assertEqual(expected_objects, total_objects_instock, "создана не уникальная запись в instock")

    def test_update_volume_object_instock(self):
        """Проверка изменения сушествующего объекта"""
        Client.my_client.post("/arrival/", data=self.data_to_instock, content_type="application/json")
        object_volume = Client.my_client.get("/instock/").data[0]["volume"]
        new_volume = self.data_to_instock["volume"] * self.data_to_instock["quantity"]
        expected_volume = self.base_expected_volume + new_volume
        self.assertEqual(expected_volume, object_volume, "Запись в InStock не обновлена")

    def test_retrieve_instock(self):
        """
             Проверяем retrieve метод. Возвращение правильного объекта по id.
        """
        response = Client.my_client.get(f"/instock/1/")
        expected_data_name = self.data_to_instock["name"]
        self.assertEqual(expected_data_name, response.data['name'], "Вернулся не верный объект")


class ProductionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cat_obj = Client.my_client.post("/catalog/", data=DATA_CATALOG[0])
        PURCHASE_DATA["catalog_name"] = cls.cat_obj.data.get("id")
        cls.purchase_obj = Client.my_client.post("/purchase/", data=PURCHASE_DATA)
        cls.purchase_obj_id = cls.purchase_obj.data.get("id")
        response_purchase = Client.my_client.get(f"/purchase/{cls.purchase_obj_id}/")
        cls.data_to_instock = {
            "name": response_purchase.data["catalog_name"],
            "volume": response_purchase.data["volume"],
            "availability": True,
        }
        cls.response = Client.my_client.post("/arrival/", data=cls.data_to_instock)
        cls.data_update = {"volume": 7}
        cls.id = cls.response.data['id']


    def test_partial_update_pruduction(self):
        """Проверка изменения volume"""
        expected = 23
        Client.my_client.patch(f"/production/{self.id}/", data=self.data_update, content_type="application/json")
        response = Client.my_client.get(f"/instock/{self.id}/")
        self.assertEqual(expected, response.data["volume"], "Некорректно выполнен partial upd записи в Instock")
        # TODO: удаление записи


    def test_update_production(self):
        """Проверяем update записи"""
        expected = 7
        Client.my_client.put(f"/production/{self.id}/", data=self.data_update, content_type="application/json")
        response = Client.my_client.get(f"/instock/{self.id}/")
        self.assertEqual(expected, response.data["volume"], "Некорректно выполнен update записи в Instock")

