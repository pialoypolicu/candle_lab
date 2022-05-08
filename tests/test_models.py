from django.test import TestCase
from core_storage.models import Catalog, Purchase


class CatalogModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем созданную запись в качестве переменной класса
        cls.catalog_task = Catalog.objects.create(
            name='Воск wax',
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


class PurchaseModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём тестовую запись в БД
        # и сохраняем созданную запись в качестве переменной класса
        catalog_obj = Catalog.objects.create(
            name="wosk"
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
