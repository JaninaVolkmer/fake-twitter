import pytest
from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status

from users.models import Follow, Token, User


def test_create_user(client, temporary_avatar):
    url = reverse("users:users")
    response = client.post(
        url,
        data={
            "username": "tessy",
            "first_name": "Tessy",
            "last_name": "Tester",
            "email": "tessy@test.com",
            "password": "tessythetester123",
            "avatar": temporary_avatar,
        },
    )
    user = User.objects.get(username="tessy")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "tessy"
    assert response.data["email"] == "tessy@test.com"
    assert response.data["first_name"] == "Tessy"
    assert response.data["last_name"] == "Tester"
    assert user.is_active == False
    assert Token.objects.filter(user=user).exists()
    assert response.data["avatar"] is not None


def test_list_user(client):
    User.objects.create(
        username="tessy1",
        first_name="Tessy1",
        last_name="Tester1",
        email="tessy1@test.com",
    )

    url = reverse("users:userlist")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


def test_retrieve_user(client):
    user = User.objects.create(
        username="tessy", first_name="Tessy", last_name="Tester", email="tessy@test.com"
    )
    url = reverse("users:userdetail", kwargs={"pk": user.pk})
    data = {
        "username": "tessy",
        "first_name": "Tessy",
        "last_name": "Tester",
        "email": "tessy@test.com",
        "password": "tessythetester123",
    }

    response = client.get(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "tessy"
    assert response.data["first_name"] == "Tessy"
    assert response.data["last_name"] == "Tester"
    assert response.data["email"] == "tessy@test.com"


def test_update_user(client):
    user = User.objects.create(
        username="elmar", first_name="Elmar", last_name="Test", email="elmar@test.com"
    )
    url = reverse("users:userdetail", kwargs={"pk": user.pk})
    data = {
        "username": "tessy",
        "first_name": "Tessy",
        "last_name": "Tester",
        "email": "tessy@test.com",
        "password": "tessythetester123",
    }

    response = client.put(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "tessy"
    assert response.data["first_name"] == "Tessy"
    assert response.data["last_name"] == "Tester"
    assert response.data["email"] == "tessy@test.com"


def test_partial_update_user(client):
    user = User.objects.create(
        username="tesmanian",
        first_name="Tessy",
        last_name="Tester",
        email="tessy@test.com",
    )
    url = reverse("users:userdetail", kwargs={"pk": user.pk})
    data = {
        "username": "tessy",
        "first_name": "Tessy",
        "last_name": "Tester",
        "email": "tessy@test.com",
        "password": "tessythetester123",
    }

    response = client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "tessy"
    assert response.data["first_name"] == "Tessy"
    assert response.data["last_name"] == "Tester"
    assert response.data["email"] == "tessy@test.com"


def test_delete_user(client):
    user = User.objects.create(
        username="elmar", first_name="Elmar", last_name="Test", email="elmar@test.com"
    )
    url = reverse("users:userdetail", kwargs={"pk": user.pk})
    data = {
        "username": "elmar",
        "first_name": "Elmar",
        "last_name": "Test",
        "email": "elmar@test.com",
        "password": "elmarthetester123",
    }

    response = client.delete(url, data=data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.filter(pk=user.pk).exists() == False


def test_follow_user(client):
    user = User.objects.get(username="testuser")
    followed = User.objects.create(
        username="elmar", first_name="Elmar", last_name="Test", email="elmar@test.com"
    )

    url = reverse("users:follows", kwargs={"pk": followed.pk})

    response = client.put(url)
    assert response.status_code == status.HTTP_200_OK
    assert user.follows.exists() == True


def test_follow_yourself_not_allowed():
    user = User.objects.create(username="tester")
    with pytest.raises(IntegrityError):
        Follow.objects.create(user=user, follows=user)


def test_unfollow_user(client):
    user = User.objects.get(username="testuser")
    followed = User.objects.create(
        username="elmar", first_name="Elmar", last_name="Test", email="elmar@test.com"
    )
    # add follow -> so we have a follower to delete
    user.follows.add(followed)

    url = reverse("users:follows", kwargs={"pk": followed.pk})

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.follows.exists() == False


def test_retrieve_token_verify(client):
    # create user with create view
    # retrieve the created user
    url = reverse("users:users")
    response = client.post(
        url,
        data={
            "username": "tessy",
            "first_name": "Tessy",
            "last_name": "Tester",
            "email": "tessy@test.com",
            "password": "tessythetester123",
        },
    )
    # user is still not active
    user = User.objects.get(username="tessy")
    # check if given user has a token
    token = Token.objects.get(user=user)
    url = reverse("users:tokenverify", kwargs={"value": token.value})

    response = client.get(url)
    # user get activated
    user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert user.is_active == True
    assert Token.objects.filter(user=user).exists()
