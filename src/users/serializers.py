from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Token, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password", "avatar")

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ()
