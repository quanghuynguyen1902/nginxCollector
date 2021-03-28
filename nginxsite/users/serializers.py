
from rest_framework import serializers
from users.models import User
from errors.api.serializers.error_log_serializers import CustomModelSerializer, SerializerValidationError

class UserSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'slug', 'created_at', 'last_login', "api_identify", "authorization_field"]

        read_only_fields = ['slug', 'email', 'password']
        extra_kwargs = {
            'authorization_field': {'write_only': True},
            'api_identify': {'write_only': True}
        }

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # try:
        #     user.set_password(validated_data['password'])
        #     user.save()
        # except KeyError:
        #     pass
        return user

class AppKeySerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'slug', 'created_at', 'last_login', "app_id", "api_identify", "authorization_field"]

        # read_only_fields = ['slug', 'email', 'password']
        # extra_kwargs = {'password': {'write_only': True}}



class UserCreateSerializer(CustomModelSerializer):
    # id = serializers.ReadOnlyField()

    password = serializers.CharField(write_only=True, required=True, style={
        "input_type": "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password is None:
            raise SerializerValidationError(field="password", code="required")
        if password2 is None:
            raise SerializerValidationError(field="password2", code="required")
        if password != password2:
            raise SerializerValidationError(field="password", code="unmatch")
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

class ApiAndAuthorizationSerializer(serializers.Serializer):
    model = User
    api_identify = serializers.CharField(required=True)
    authorization_field = serializers.CharField(required=True)