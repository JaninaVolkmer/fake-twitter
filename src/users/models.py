import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# define where you want to upload the avatar
# return the fact that you want to save that image to the users folder + utilize the filename
def upload_to(instance, filename):
    return "users/{filename}".format(filename=filename)


class User(AbstractUser):
    follows = models.ManyToManyField(
        "self",
        symmetrical=False,
        through="Follow",
    )
    avatar = models.ImageField(upload_to=upload_to, default="users/default.jpg")


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follows = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "follows"], name="unique_relationship"
            ),
            models.CheckConstraint(
                name="prevent_self_follow", check=~models.Q(user=models.F("follows"))
            ),
        ]


def random_hex():
    return secrets.token_hex(16)


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SlugField(max_length=32, unique=True, default=random_hex)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "value"], name="unique_together")
        ]
