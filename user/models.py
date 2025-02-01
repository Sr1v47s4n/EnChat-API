from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

DEFAULT_PROFILE_PICS = [
    "default_profile_pics/_1.png",
    "default_profile_pics/_2.png",
    "default_profile_pics/_3.png",
    "default_profile_pics/_4.png",
    "default_profile_pics/_5.png",
    "default_profile_pics/_6.png",
]


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, profile_picture=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)

        # Assign default profile picture if not chosen
        if profile_picture and profile_picture in DEFAULT_PROFILE_PICS:
            user.profile_picture = profile_picture
        else:
            user.profile_picture = DEFAULT_PROFILE_PICS[0]  # Default to first image

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    profile_picture = models.CharField(
        max_length=100, choices=[(pic, pic) for pic in DEFAULT_PROFILE_PICS]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
