from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core_storage.models import Catalog, InStock, Purchase
from core_storage.serializers import (CatalogSerializer, ArrivalInStockSerializer,
                                      PurchaseSerializer, InStockSerializer)


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

class UpdateDestroyViewSet(
    mixins.UpdateModelMixin,
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
    queryset = InStock.objects.all()
    serializer_class = ArrivalInStockSerializer

    def create(self, request, **kwargs):
        data = request.data
        try:
            obj = InStock.objects.get(name=data.get("name"))
            serializer = ArrivalInStockSerializer(data=data, instance=obj)
        except ObjectDoesNotExist:
            serializer = ArrivalInStockSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductionViewSet(UpdateDestroyViewSet):
    queryset = InStock.objects.all()
    serializer_class = ArrivalInStockSerializer


# class ProductionViewSet(EnablePartialUpdateMixin, UpdateDestroyViewSet):
#     # TODO установить пермишены. метод update для супер юзера, partial для всех зареганных
#     queryset = InStock.objects.all()
#     serializer_class = InStockSerializer
#
#     def partial_update(self, request, *args, **kwargs):
#         kwargs['partial'] = True
#         obj = get_object_or_404(self.queryset, pk=kwargs['pk'])
#         request.data["volume"] = obj.volume - request.data["volume"]
#         return self.update(request, *args, **kwargs)
