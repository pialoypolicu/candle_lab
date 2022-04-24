from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core_storage.core_storage_orm.orm_play import create_position_in_purchase, create_or_update_arrival_wait
from pprint import pprint


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

