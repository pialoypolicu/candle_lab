from django.db import models


class Purchase(models.Model):
    name = models.CharField("Название", max_length=256)
    date_purchase = models.DateField("День покупки")
    quantity = models.PositiveSmallIntegerField("Количество")
    weight = models.PositiveIntegerField("Вес, гр")
    price = models.FloatField("Цена")
