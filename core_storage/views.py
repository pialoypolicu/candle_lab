import json
from pprint import pprint
from http import HTTPStatus
from django.forms import model_to_dict
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view
from core_storage.models import Catalog, Purchase, InStock
from core_storage.serializers import CatalogSerializer, PurchaseSerializer, InStockSerializer
from core_storage.core_storage_orm.orm_play import create_or_update_instock


class CreateRetrieveListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class ListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class CreateUpdateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CatalogViewSet(CreateRetrieveListViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class PurchaseViewSet(CreateRetrieveListViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class InStockViewSet(ListViewSet):
    queryset = InStock.objects.all()
    serializer_class = InStockSerializer


class ArrivalViewSet(viewsets.ViewSet):
    queryset = InStock.objects.all()
    serializer_class = InStockSerializer

    def create(self, request):
        queryset = InStock.objects.filter(name=request.data["name"])
        if queryset.exists():
            volume = queryset.first().volume + int(request.data["volume"])
            obj, result = queryset.update_or_create(name=request.data["name"], defaults={'volume': volume})
            serializer = InStockSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = InStockSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
