from django.urls import path
from .views import register_account, sign_in
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("stats/", views.stats, name="stats"),
    path("login/", views.login_view, name="login"),
    path("register_post/", views.register_post, name="register_post"),
    path("users/", views.users, name="users"),
    path("register_account/", register_account, name="register_account"),
    path("sign_in/", sign_in, name="sign_in"),
]