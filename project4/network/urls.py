
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:user_id>", views.user, name="user"),
    path("follow/<str:page_user_id>", views.follow, name="follow"),
    path("unfollow/<str:page_user_id>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),

    path("edit", views.edit_post, name="edit"),
    path("like", views.like_post, name="like"),
    path("post_likes/<str:post_id>", views.post_likes, name="post_likes"),
]
