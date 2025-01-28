from django.urls import path
from .views import register_account, sign_in, user_picked_option, get_user_picked_options
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("stats/", views.stats, name="stats"),
    path("login/", views.login_view, name="login"),
    path("register_post/", views.register_post, name="register_post"),
    path("users/", views.users, name="users"),
    path("register_account/", register_account, name="register_account"),
    path("sign_in/", sign_in, name="sign_in"),
    path("matches/", views.matches, name="matches"),
    path('user_picked_option/', user_picked_option, name='user_picked_option'),
    path('get_user_picked_options/', get_user_picked_options, name='get_user_picked_options'),
    path('odds') # TODO: add odds view
]