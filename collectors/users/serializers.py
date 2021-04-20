from .models import UsersUser
from rest_framework import serializers

class AppKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersUser
        fields = ['id', 'username', 'email', 'slug', 'created_at', 'last_login', "app_id", "api_identify", "authorization_field"]
