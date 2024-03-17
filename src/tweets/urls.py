from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tweets import views

app_name = "tweets"
urlpatterns = [
    path("", views.TweetCreate.as_view(), name="tweets"),
    path("list", views.TweetList.as_view(), name="tweetlist"),
    path("select/", views.TweetUserList.as_view(), name="select"),
    path("likes/<int:pk>", views.Likes.as_view(), name="likes"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
