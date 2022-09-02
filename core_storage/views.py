from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from core_storage.models import Catalog, Purchase, InStock
from core_storage.serializers import CatalogSerializer, PurchaseSerializer, InStockSerializer


class EnablePartialUpdateMixin:
    """Enable partial updates

    Override partial kwargs in UpdateModelMixin class
    https://github.com/encode/django-rest-framework/blob/91916a4db14cd6a06aca13fb9a46fc667f6c0682/rest_framework/mixins.py#L64
    """
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


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


class InStockViewSet(ListRetrieveViewSet):
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


class ProductionViewSet(EnablePartialUpdateMixin, UpdateDestroyViewSet):
    # TODO установить пермишены. метод update для супер юзера, partial для всех зареганных
    queryset = InStock.objects.all()
    serializer_class = InStockSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        obj = get_object_or_404(self.queryset, pk=kwargs['pk'])
        request.data["volume"] = obj.volume - request.data["volume"]
        return self.update(request, *args, **kwargs)
