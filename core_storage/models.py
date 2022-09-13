from django.db import models
from django.utils.translation import gettext_lazy as _


class CategoryChoice(models.TextChoices):
    WAX = 'WAX', _('Wax')
    PERFUME = 'PERF', _('Perfume')
    WICK = "WICK", _("Wick")
    NONE = 'NONE', _("None")


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class ArrivalChoice(models.TextChoices):
    ARR = 'ARR', _('arrived')
    WAY = 'WAY', _('on the way')
    NONE = 'NONE', _("None")


class Purchase(models.Model):
    # TODO: упорядоченость по дате
    """Закупка материала"""
    catalog_name = models.ForeignKey(
        "Catalog",
        on_delete=models.PROTECT,
        verbose_name="Каталожное название",
        related_name="purchases"
    )
    name = NameField("Название", max_length=256)
    volume = models.PositiveIntegerField("Вес/кол-во, гр/шт")
    company = NameField("Название поставщика", max_length=256)
    date_purchase = models.DateField("День покупки")
    quantity = models.PositiveSmallIntegerField("Количество")
    price = models.FloatField("Цена")
    comment = models.CharField(max_length=256, null=True, verbose_name="комментарии")
    arrival = models.CharField(
        max_length=4,
        choices=ArrivalChoice.choices,
        default=ArrivalChoice.WAY,
        null=True,
        verbose_name="Статус прибытия"
    )
    instock = models.OneToOneField("InStock", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.catalog_name.name


class InStock(models.Model):
    """На складе"""
    name = NameField("Название", max_length=256, unique=True)
    volume = models.PositiveIntegerField("Вес/кол-во, гр/шт")
    availability = models.BooleanField("Наличие", blank=True, null=True, default=True)
    update_date = models.DateTimeField("Дата обновления", auto_now=True)

    def __str__(self):
        return self.name


class Catalog(models.Model):
    """Список материалов, который доступен для заказа"""
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
