from rest_framework import generics
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Tweet
from .serializers import LikesSerializer, TweetSerializer


class TweetCreate(generics.CreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class TweetList(generics.ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    # return tweets the author owns
    def get_queryset(self):
        user = self.request.user
        return Tweet.objects.filter(author=user)


# select specific user tweets + list all tweets
class TweetUserList(generics.ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        author = self.request.query_params.get("author")
        if author is not None:
            return Tweet.objects.filter(author=author)
        return Tweet.objects.all()


class Likes(UpdateAPIView, DestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_update(self, serializer):
        user = self.request.user
        tweet = self.get_object()
        tweet.likes.add(user)

        # return parent class object & update it
        return super().perform_update(serializer)

    def perform_destroy(self, serializer):
        user = self.request.user
        tweet = self.get_object()
        tweet.likes.remove(user)

        return super().perform_destroy(serializer)
