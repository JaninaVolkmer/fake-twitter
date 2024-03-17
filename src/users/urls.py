from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from users import views

app_name = "users"
urlpatterns = [
    path("", views.UserCreate.as_view(), name="users"),
    path("list", views.UserList.as_view(), name="userlist"),
    path("detail/<int:pk>", views.UserDetail.as_view(), name="userdetail"),
    path("follows/<int:pk>", views.Follows.as_view(), name="follows"),
    # create url to verify token
    path(
        "tokenverify/<slug:value>",
        views.TokenVerifyView.as_view(),
        name="tokenverify",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
