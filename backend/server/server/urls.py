from django.urls import path
from .views import register_account, sign_in

urlpatterns = [
    path('register/', register_account, name='register_account'),
    path('signin/', sign_in, name='sign_in'),
]