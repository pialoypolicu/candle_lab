from django.contrib import admin
from core_storage.models import Purchase, InStock, Catalog


class PurchaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Purchase._meta.get_fields()]


class InStockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in InStock._meta.get_fields()]


class CatalogAdmin(admin.ModelAdmin):
    list_display = ["name", "volume", "company", "category"]


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(InStock, InStockAdmin)
admin.site.register(Catalog, CatalogAdmin)
