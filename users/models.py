from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
        Custom User Model
    """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_ATHOR = "athor"

    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_ATHOR, "Athor"),
    ]

    LOGIN_EMAIL = "email"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = [
        (LOGIN_EMAIL, "Email"),
        (LOGIN_KAKAO, "Kakao"),
    ]

    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=10,
        blank=False,
        null=False,
        default=GENDER_MALE,
    )

    login_method = models.CharField(
        max_length=10,
        choices=LOGIN_CHOICES,
        default=LOGIN_EMAIL,
        blank=False,
        null=False,
    )

    rating = models.IntegerField(default=10)

    def __str__(self):
        return self.first_name
