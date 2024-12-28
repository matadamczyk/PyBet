from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("stats/", views.stats, name="stats"),
    path("login/", views.login_view, name="login"),
    path("login_post/", views.login_post, name="login_post"),
    path("users/", views.users, name="users")
]