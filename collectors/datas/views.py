from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from module import collector
from .permissions import CheckAppKey
from rest_framework.permissions import IsAuthenticated, AllowAny


    
class DataRaw(APIView):
    permission_classes = [CheckAppKey]
    def post(self, request, format=None):
        app_key = request.META.get('HTTP_APP_KEY')
        data=request.data['data']
        collector.write_data(data, app_key)
        return Response({"message": "success"})