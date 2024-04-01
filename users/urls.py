from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import SignUp, profile, get_user_profile, user_search, send_friend_request, accept_friend_request, edit_profile, user_friends_posts, unfollow, unsend_request, user_friends_posts_pgntd


app_name="users"

urlpatterns = [
    path('signup/', SignUp.as_view(template_name='signup.html'), name='signup'),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile", profile, name="profile"),
    path("profile/edit_profile", edit_profile, name="edit_profile"),
    path("<int:user_id>", get_user_profile, name="get_user_profile"),
    path("user_search", user_search, name="user_search"),
    path("send_friend_request/<int:other_user_id>",send_friend_request, name="send_friend_request"),
    path("unsend_request/<int:user_id>",unsend_request, name="unsend_request"),
    path("accept_friend_request/<int:other_user_id>",accept_friend_request, name="accept_friend_request"),
    path("unfollow/<int:user_id>", unfollow, name="unfollow"),

    # paginated and un paginated posts => list and view_posts
    # path("view_posts",user_friends_posts, name="user_friends_posts"),
    path("list",user_friends_posts_pgntd, name="user_friends_posts_pgntd"),
]