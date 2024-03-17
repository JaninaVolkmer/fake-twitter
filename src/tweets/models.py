from django.db import models

from users.models import User

# Create your models here.


class Tweet(models.Model):
    author = models.ForeignKey(User, related_name="tweets", on_delete=models.CASCADE)
    text = models.CharField(max_length=128, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through="Like")


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "tweet")
