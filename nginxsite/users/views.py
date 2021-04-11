from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserCreateSerializer, UserSerializer, AppKeySerializer, ApiAndAuthorizationSerializer, CustomTokenObtainPairSerializer
from .models import User
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import CheckAppKey

class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    lookup_field = "slug"
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
 
    @action(methods=['PUT'], detail=True, permission_classes=[IsAuthenticated], url_path='update-user')
    def update_api_identify_and_authorization_key(self, request, *args, **kwargs):
        serializer = ApiAndAuthorizationSerializer(data=request.data)
        if not serializer.is_valid():
            return None
        api_identify = serializer.data.get('api_identify')
        authorization_field = serializer.data.get('authorization_field')
        user = self.request.user
        user.api_identify = api_identify
        user.authorization_field = authorization_field
        user.save()
        return Response({"message": "success"})
        



class UserViewByAppKey(APIView):
    permission_classes = [CheckAppKey]

    def get(self, request):
        app_key = request.META.get('HTTP_APP_KEY')
        user = User.objects.get(app_key=app_key)
        serializer = AppKeySerializer(user)
        return Response(serializer.data)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
