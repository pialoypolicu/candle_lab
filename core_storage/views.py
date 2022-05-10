import json
from pprint import pprint
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view
from core_storage.models import Catalog, Purchase, ArrivalWait
from core_storage.serializers import CatalogSerializer, PurchaseSerializer, ArrivalWaitSerializer

from core_storage.core_storage_orm.orm_play import create_or_update_arrival_wait, create_or_update_instock, delete_or_update_arrival_wait


class CreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class PurchaseViewSet(CreateListViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        serializer_purchase = self.get_serializer(data=request.data)
        serializer_purchase.is_valid(raise_exception=True)
        self.perform_create(serializer_purchase)
        headers = self.get_success_headers(serializer_purchase.data)
        result = create_or_update_arrival_wait(serializer_purchase.validated_data)
        if result['result'] != "error":
            serialized_arival_wait = model_to_dict(result['result'])
            return Response(
                [serializer_purchase.data, serialized_arival_wait],
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(
            [serializer_purchase.data, result["message"]],
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ArivalAwaitViewSet(CreateListViewSet):
    queryset = ArrivalWait.objects.all()
    serializer_class = ArrivalWaitSerializer


class PinMaterial(APIView):
    def post(self, request):
        data = request.data

class ArrivalMaterial(APIView):
    def post(self, request):
        data = request.data
        response = create_or_update_instock(data)
        result_arriva_object = delete_or_update_arrival_wait(data)
        if response == 1:
            return Response({"result": data, "result_arriva_object": result_arriva_object}, status=status.HTTP_200_OK)
        return Response({"result": model_to_dict(response), "result_arriva_object": result_arriva_object}, status=status.HTTP_200_OK)


@api_view(['GET', "POST"])
def catalog_view(request):
    if request.method == "POST":
        serializer = CatalogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    catalog_items = Catalog.objects.all()
    serializer = CatalogSerializer(catalog_items, many=True)
    return Response(serializer.data)
