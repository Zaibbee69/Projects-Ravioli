
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # Url if user want to create new posts
    path("newpost", views.new_post, name="new_post"),

    # path for the personal users id
    path("profile/<str:username>", views.profile_user, name="profile_user"),

    # path for the user who want to follow unfollow someone
    path("profile/<str:username>/follow", views.toggle_follow, name="toggle_follow"),

    # path when user want to access his followings post
    path("following", views.following, name="following"),

    # path for users when they wanna edit a post
    path("post/<str:post_id>/edit", views.edit_post, name="edit_post"),

    # path for users who wanna like a post
    path("post/<str:post_id>/like", views.like_post, name="like_post")
]
