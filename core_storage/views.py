from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core_storage.models import Catalog

from core_storage.core_storage_orm.orm_play import create_position_in_purchase, create_or_update_arrival_wait, create_or_update_instock, delete_or_update_arrival_wait


class CreatePurchase(APIView):
    def post(self, request):
        data = request.data
        created_object = create_position_in_purchase(data=data)
        if created_object:
            response = create_or_update_arrival_wait(data)
        if response == 1:
            response = model_to_dict(created_object)
        else:
            response = model_to_dict(response)
        return Response({"message": response}, status=status.HTTP_200_OK)


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


class GetCatalog(APIView):
    def get(self, request):
        object = Catalog.objects.first()
        object = model_to_dict(object)
        return Response({'result': object})
