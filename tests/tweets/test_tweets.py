from django.urls import reverse
from rest_framework import status

from tweets.models import Like, Tweet
from users.models import User


def test_create_tweet(client):
    author = User.objects.create(
        username="elmar", first_name="Elmar", last_name="Test", email="elmar@test.com"
    )

    url = reverse("tweets:tweets")
    data = {
        "author": author.pk,
        "text": "hello my friend",
    }
    response = client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["text"] == "hello my friend"


def test_author_owns_tweet(client):
    author = User.objects.get(username="testuser")
    Tweet.objects.create(author=author, text="hello")
    Tweet.objects.create(author=author, text="hello again")
    url = reverse("tweets:tweetlist")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


def test_select_user_tweet(client):
    author = User.objects.create(username="testuser23")
    Tweet.objects.create(author=author, text="hello")
    Tweet.objects.create(author=author, text="hello again")

    url = reverse("tweets:select")
    url = f"{url}?author={author.pk}"

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


def test_likes_tweet(client):
    author = User.objects.get(username="testuser")
    tweet = Tweet.objects.create(author=author, text="hello")
    url = reverse("tweets:likes", kwargs={"pk": tweet.pk})

    response = client.put(url)
    tweet.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert Like.objects.filter(tweet=tweet).count() == 1


def test_delete_like_tweet(client):
    author = User.objects.get(username="testuser")
    tweet = Tweet.objects.create(author=author, text="hello")
    # add like -> so we have a like to delete
    tweet.likes.add(author)

    url = reverse("tweets:likes", kwargs={"pk": tweet.pk})

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert tweet.likes.exists() == False
