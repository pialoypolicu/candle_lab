from pprint import pprint
from tests.constants import DATA_CATALOG
from django.test import TestCase, Client
from core_storage.models import Catalog, Purchase
from tests.constants import PURCHASE_DATA


class CatalogModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.catalog_obj = Catalog.objects.create(**DATA_CATALOG[0])

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = self.catalog_obj
        field_verboses = {
            'name': 'Название',
            "volume": "Вес/кол-во, гр/шт",
            "company": "Название поставщика",
            "category": "Категория"
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test__str__text(self):
        """__str__ text в полях совпадает с ожидаемым."""
        task = self.catalog_obj
        expected_text = task.name
        self.assertEqual(expected_text, str(task))

    # def test_choice_category(self):
    #     task = CatalogModelTest.catalog_task
    #     choices_field = {
    #         "category": "WAX"
    #     }
    #     response = Client().get("/catalog/")
    #     for field, expected_value in choices_field.items():
    #         with self.subTest(field=field):
    #             cat = task._meta.get_field(field)
    #             pprint(dir(cat))
    #             m = cat.choices
    #             get_c = cat.get_choices()
    #             c = task.category
    #             self.assertEqual(
    #                 task._meta.get_field(field).verbose_name, expected_value)


class PurchaseModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.my_client = Client()
        cls.catalog_obj = Catalog.objects.create(
            name="wosk",
            volume=30,
            company="greenwax",
            category="WAX",
        )
        cls.purchase_task = Purchase.objects.create(
            catalog_name=cls.catalog_obj,
            date_purchase="2022-04-01",
            quantity=1,
            volume=30,
            price=1000,
        )
        PURCHASE_DATA["catalog_name"] = cls.catalog_obj.id
        cls.response = cls.my_client.post(
            "/purchase/",
            data=PURCHASE_DATA,
            content_type='application/json',
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = PurchaseModelTest.purchase_task
        field_verboses = {
            'catalog_name': 'Каталожное название',
            "date_purchase": "День покупки",
            "quantity": "Количество",
            "volume": "Вес, гр",
            "price": "Цена",
            "comment": "комментарии",
            "arrival": "Статус прибытия",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test__str__text(self):
        """__str__ text в полях совпадает с ожидаемым."""
        task = self.purchase_task
        expected_text = task.catalog_name.name
        self.assertEqual(expected_text, str(task))

    def test_arrival(self):
        task = self.purchase_task
        expected = "WAY"
        arrival = task.arrival
        self.assertEqual(expected, arrival, "статус доставки не сопадает")

