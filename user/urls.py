from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile_pictures/", views.get_profile_pictures, name="profile_pictures"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]
