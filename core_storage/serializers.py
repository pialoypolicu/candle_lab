from rest_framework import serializers
from pprint import pprint

from core_storage.models import Catalog, Purchase, InStock


class CatalogSerializer(serializers.ModelSerializer):
    catalog_name = serializers.StringRelatedField(many=True)

    class Meta:
        model = Catalog
        fields = ("__all__")


class PurchaseSerializer(serializers.ModelSerializer):
    catalog_name = serializers.StringRelatedField()

    class Meta:
        model = Purchase
        fields = ("__all__")

    def create(self, validated_data):
        cat_name = Catalog.objects.get(pk=self.initial_data.get("catalog_name"))
        validated_data['catalog_name'] = cat_name
        purchase = Purchase.objects.create(**validated_data)
        return purchase


class InStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = InStock
        fields = ("__all__")
