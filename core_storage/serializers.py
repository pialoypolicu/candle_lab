from rest_framework import serializers

from core_storage.models import Catalog, Purchase, ArrivalWait


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"

class ArrivalWaitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalWait
        fields = "__all__"

