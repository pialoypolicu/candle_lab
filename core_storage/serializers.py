from django.core import exceptions
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from core_storage.core_storage_orm.orm_play import update_db

from candle_lab.logger import Logger
from core_storage.models import Catalog, InStock, Purchase

logmngr = Logger(directory="core_storage", file="serializers")


class CatalogSerializer(serializers.ModelSerializer):
    # purchases = serializers.StringRelatedField(many=True, required=False)
    class Meta:
        model = Catalog
        fields = ("__all__")


class PurchaseSerializer(serializers.ModelSerializer):
    catalog_name = serializers.StringRelatedField()

    class Meta:
        model = Purchase
        fields = ("id", "name", "company", "date_purchase", "quantity", "volume", "price", "comment", "arrival", "catalog_name")

    def create(self, validated_data):
        name = validated_data["name"].lower()
        volume = validated_data["volume"]
        company = validated_data["company"].lower()
        try:
            # todo get_object_or_404
            catalog_obj = Catalog.objects.get(Q(name=name) & Q(volume=volume) & Q(company=company))
        except exceptions.ObjectDoesNotExist:
            logmngr.logger.warning("object not exists", name=name)
            raise serializers.ValidationError(detail=f"Catalog object - {name} not exists", code='core_storage.serializers')
        catalog_obj_id = catalog_obj.id
        validated_data["catalog_name_id"] = catalog_obj_id
        obj = Purchase.objects.create(**validated_data)
        return obj


class InStockSerializer(serializers.ModelSerializer):
    # purchase = PurchaseSerializer(read_only=True)

    class Meta:
        model = InStock
        fields = ("id", "name", "volume", "purchase", "availability","update_date")


class ArrivalInStockSerializer(serializers.ModelSerializer):
    purchase = PurchaseSerializer(read_only=True)
    quantity = serializers.IntegerField(write_only=True, required=True)
    company = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = InStock
        fields = ("id", "name", "volume", "purchase", "availability", "update_date", "quantity", "company")

    def create(self, validated_data):
        name = validated_data["name"].lower()
        volume = validated_data["volume"]
        company = validated_data.pop("company").lower()
        quantity = validated_data.pop("quantity")
        purchase_object = get_object_or_404(Purchase, name=name, volume=volume, company=company)
        validated_data["volume"] = quantity * volume
        instance = InStock.objects.create(**validated_data)
        update_db(purchase_object, quantity)
        return instance

    def update(self, instance, validated_data):
        name = validated_data["name"].lower()
        volume = validated_data["volume"]
        company = validated_data.pop("company").lower()
        quantity = validated_data.pop("quantity")
        instance.volume = quantity * volume + instance.volume
        instance.save()
        purchase_object = get_object_or_404(Purchase, name=name, volume=volume, company=company)
        update_db(purchase_object, quantity)
        return instance

