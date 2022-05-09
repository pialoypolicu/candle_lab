from pprint import pprint

from django.test import TestCase, Client
from core_storage.models import Catalog, Purchase


class CatalogModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.catalog_task = Catalog.objects.create(
            name='Воск wax',
            weight=30,
            company="greenwax",
            category=Catalog.CategoryChoice("PERF")
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = CatalogModelTest.catalog_task
        field_verboses = {
            'name': 'Название',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test__str__text(self):
        """__str__ text в полях совпадает с ожидаемым."""
        task = CatalogModelTest.catalog_task
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
        catalog_obj = Catalog.objects.create(
            name="wosk",
            weight=30,
            company="greenwax",
            category="WAX",
        )
        cls.purchase_task = Purchase.objects.create(
            name="Воск wax",
            date_purchase="2022-04-01",
            quantity=1,
            weight=30,
            price=1000,
            catalog_name=catalog_obj
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = PurchaseModelTest.purchase_task
        field_verboses = {
            'name': 'Название',
            "date_purchase": "День покупки",
            "quantity": "Количество",
            "weight": "Вес, гр",
            "price": "Цена",
            "catalog_name": "Каталожное название",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test__str__text(self):
        """__str__ text в полях совпадает с ожидаемым."""
        task = CatalogModelTest.catalog_task
        expected_text = task.name
        self.assertEqual(expected_text, str(task))
