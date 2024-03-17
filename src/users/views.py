from django.http import Http404
from rest_framework import generics, status
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Token, User
from .serializers import TokenSerializer, UserFollowSerializer, UserSerializer

# Create your views here.


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)
        user.is_active = False
        user.save()


class TokenVerifyView(generics.RetrieveAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [
        AllowAny,
    ]

    # execute if token matches if yes. change active=True
    def retrieve(self, request, *args, **kwargs):
        received_token = kwargs.get("value")
        # check if token exists
        try:
            token_user = Token.objects.get(value=received_token)
        except Token.DoesNotExist:
            raise Http404("Token does not exist")

        user = token_user.user
        # active user
        user.is_active = True
        user.save()
        return Response("Activated", status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class Follows(UpdateAPIView, DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserFollowSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_update(self, serializer):
        user = self.request.user
        followed = self.get_object()
        user.follows.add(followed)

        # return parent class object & update it
        return super().perform_update(serializer)

    def perform_destroy(self, serializer):
        user = self.request.user
        followed = self.get_object()
        user.follows.remove(followed)

        return super().perform_destroy(serializer)
