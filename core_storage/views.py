from functools import reduce
from operator import or_

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_list_or_404
from loguru import logger
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from candle_lab.logger import Logger
from core_storage.models import Catalog, InStock, Purchase
from core_storage.serializers import (ArrivalInStockSerializer,
                                      CatalogSerializer, InStockSerializer,
                                      ProductionSerializer, PurchaseSerializer)

logmngr = Logger(directory="core_storage", file="views")

class EnablePartialUpdateMixin:
    """Enable partial updates

    Override partial kwargs in UpdateModelMixin class
    https://github.com/encode/django-rest-framework/blob/91916a4db14cd6a06aca13fb9a46fc667f6c0682/rest_framework/mixins.py#L64
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class CreateUpdateViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    pass


class CreateRetrieveListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class CatalogViewSet(CreateRetrieveListViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class PurchaseViewSet(CreateRetrieveListViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class InStockViewSet(ListRetrieveViewSet):
    queryset = InStock.objects.all()
    serializer_class = InStockSerializer


class ArrivalViewSet(CreateUpdateViewSet):
    serializer_class = ArrivalInStockSerializer

    def get_queryset(self, data):
        try:
            return InStock.objects.get(name=data.get("name"))
        except ObjectDoesNotExist:
            # todo logger
            return None

    def create(self, request, *args, **kwargs):
        data = self.request.data
        instock_object = self.get_queryset(data)
        if instock_object:
            serializer = ArrivalInStockSerializer(data=data, instance=instock_object)
            response_status = status.HTTP_200_OK
        else:
            serializer = ArrivalInStockSerializer(data=data)
            response_status = status.HTTP_201_CREATED
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=response_status)


class ProductionViewSet(viewsets.ViewSet):
    serializer_class = ProductionSerializer
    def update(self, request):
        instances = list()
        data = request.data
        data = {item.pop("name"): item for item in data}
        names = list(data.keys())
        query = reduce(or_, (Q(name=key) for key in names))
        queryset = get_list_or_404(InStock, query)
        for q in queryset:
            serializer = ProductionSerializer(q, data=data[q.name], partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                instances.append(serializer.data)
            except Exception as e:
                logmngr.logger.warning(e)
        return Response(instances)
