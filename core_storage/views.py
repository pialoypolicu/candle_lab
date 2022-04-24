from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core_storage.core_storage_orm.orm_play import create_position


class APICat(APIView):
    def post(self, request):
        data = request.data
        response = create_position(data=data)
        return Response({"message": response})
