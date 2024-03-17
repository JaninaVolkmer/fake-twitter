from rest_framework import serializers

from tweets.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ("author", "text", "date_created")


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ()
