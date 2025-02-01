from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile_pictures/", views.get_profile_pictures, name="profile_pictures"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]
