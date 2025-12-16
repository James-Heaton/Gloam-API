from django.urls import path
from .views.auth import register_user, login_user

urlpatterns = [
    path("register", register_user, name="register"),
    path("login", login_user, name="login"),
]
