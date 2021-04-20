from .serializers import AppKeySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UsersUser
from datas.permissions import CheckAppKey

class UserViewByAppKey(APIView):
    permission_classes = [CheckAppKey]

    def get(self, request):
        app_key = request.META.get('HTTP_APP_KEY')
        user = UsersUser.objects.get(app_key=app_key)
        serializer = AppKeySerializer(user)
        return Response(serializer.data)