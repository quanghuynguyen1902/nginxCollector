from rest_framework.permissions import BasePermission
from users.models import UsersUser

class CheckAppKey(BasePermission):
    def has_permission(self, request, view):
        # API_KEY should be in request headers to authenticate requests
        app_key = request.META.get('HTTP_APP_KEY')
        user = UsersUser.objects.filter(app_key=app_key).exists()
        return user
