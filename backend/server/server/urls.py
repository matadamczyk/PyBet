from django.urls import path
from .views import register_account, sign_in

urlpatterns = [
    path("", views.home, name="home"),
    path("stats/", views.stats, name="stats"),
    path("login/", views.login_view, name="login"),
    path("login_post/", views.login_post, name="login_post"),
    path("users/", views.users, name="users")
]