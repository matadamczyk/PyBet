from django.urls import path
from .views import (
    register_account,
    sign_in,
    user_picked_option,
    get_user_picked_options,
    get_profitable_odds,
    add_pycoins,
    place_bet,
    get_user_pycoins,
)
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
    path("user_picked_option/", user_picked_option, name="user_picked_option"),
    path(
        "get_user_picked_options/",
        get_user_picked_options,
        name="get_user_picked_options",
    ),
    path("profitable/", get_profitable_odds, name="get_profitable_odds"),
    path("add-pycoins/", views.add_pycoins, name="add_pycoins"),
    path("place-bet/", views.place_bet, name="place_bet"),
    path("user-pycoins/", views.get_user_pycoins, name="get_user_pycoins"),
]
