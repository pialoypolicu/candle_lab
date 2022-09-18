from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from candle_lab.logger import Logger
from core_storage.models import Catalog, InStock, Purchase

logmngr = Logger(directory="core_storage", file="serializers")


class CatalogSerializer(serializers.ModelSerializer):
    # catalog_name = serializers.StringRelatedField(many=True, required=False)
    class Meta:
        model = Catalog
        fields = ("__all__")


class PurchaseSerializer(serializers.ModelSerializer):
    catalog_name = serializers.StringRelatedField()

    class Meta:
        model = Purchase
        fields = ("id", "name", "company", "date_purchase", "quantity", "volume", "price", "comment", "arrival", "catalog_name")

    def create(self, validated_data):
        name = validated_data["name"]
        volume = validated_data["volume"]
        company = validated_data["company"]
        try:
            catalog_obj = Catalog.objects.get(Q(name=name) & Q(volume=volume) & Q(company=company))
            catalog_obj_id = catalog_obj.id
            validated_data["catalog_name_id"] = catalog_obj_id
            obj = Purchase.objects.create(**validated_data)
            return obj
        except exceptions.ObjectDoesNotExist as error:
            logmngr.logger.warning("object not exists", name=name)
            raise ParseError(detail=f"object - {name} not exists", code='core_storage.serializers')


class InStockSerializer(serializers.ModelSerializer):
    purchase = PurchaseSerializer(read_only=True)
    class Meta:
        model = InStock
        fields = ("name", "volume", "purchase", "availability", "update_date")
    # TODO что то сделать с проверкой поля quantity
    def create(self, validated_data):
        validated_data["volume"] = self.initial_data["quantity"] * validated_data["volume"]
        instance = InStock.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        volume = self.initial_data["quantity"] * validated_data["volume"] + instance.volume
        instance.volume = volume
        instance.save()
        return instance

