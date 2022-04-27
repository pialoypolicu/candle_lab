from django.db import models


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Purchase(models.Model):
    """Закупка материала"""
    name = NameField("Название", max_length=256)
    date_purchase = models.DateField("День покупки")
    quantity = models.PositiveSmallIntegerField("Количество")
    weight = models.PositiveIntegerField("Вес, гр")
    price = models.FloatField("Цена")
    catalog_name = models.ForeignKey("Catalog", on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class InStock(models.Model):
    """На складе"""
    name = NameField("Название", max_length=256)
    weight = models.PositiveIntegerField("Вес, гр")
    update_date = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.name


class ArrivalWait(models.Model):
    """Ожидание заказанного материала"""
    name = NameField("Название", max_length=256)
    created_date = models.DateTimeField("Дата создания записи", auto_now_add=True)
    quantity = models.PositiveSmallIntegerField("Количество")
    weight = models.PositiveIntegerField("Вес, гр")

    def __str__(self):
        return self.name


class Catalog(models.Model):
    name = NameField("Название", max_length=256, db_index=True)

    def __str__(self):
        return self.name
