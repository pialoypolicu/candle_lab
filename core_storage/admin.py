from django.contrib import admin
from core_storage.models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Purchase._meta.get_fields()]

admin.site.register(Purchase, PurchaseAdmin)

