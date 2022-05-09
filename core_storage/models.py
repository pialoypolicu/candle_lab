from django.db import models
from django.utils.translation import gettext_lazy as _


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class Purchase(models.Model):
    """Закупка материала"""
    catalog_name = models.ForeignKey("Catalog", on_delete=models.PROTECT, null=True, verbose_name="Каталожное название")
    date_purchase = models.DateField("День покупки")
    quantity = models.PositiveSmallIntegerField("Количество")
    weight = models.PositiveIntegerField("Вес, гр")
    price = models.FloatField("Цена")
    comments = models.CharField(max_length=256, null=True, verbose_name="комментарии")

    def __str__(self):
        return self.catalog_name.name


class InStock(models.Model):
    """На складе"""
    name = NameField("Название", max_length=256)
    weight = models.PositiveIntegerField("Вес, гр")
    update_date = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.name


class ArrivalWait(models.Model):
    """Ожидание заказанного материала"""
    # name = NameField("Название", max_length=256)
    created_date = models.DateTimeField("Дата создания записи", auto_now_add=True)
    quantity = models.PositiveSmallIntegerField("Количество")
    weight = models.PositiveIntegerField("Вес, гр")
    catalog_name = models.ForeignKey("Catalog", on_delete=models.PROTECT, null=True, verbose_name="Каталожное название")

    def __str__(self):
        return self.name


class Catalog(models.Model):
    """Список материалов, который доступен для заказа"""
    class CategoryChoice(models.TextChoices):
        WAX = 'WAX', _('Wax')
        PERFUME = 'PERF', _('Perfume')
        WICK = "WICK", _("Wick")
        NONE = 'NONE', _("None")
    name = NameField("Название", max_length=256)
    volume = models.PositiveIntegerField("Вес/кол-во, гр/шт")
    company = NameField("Название поставщика", max_length=256)
    category = models.CharField(
        max_length=4,
        choices=CategoryChoice.choices,
        default=CategoryChoice.NONE,
        null=True,
        verbose_name="Категория"
    )

    class Meta:
        unique_together = ("name", "volume", "company")

    def __str__(self):
        return self.name
