import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from core import managers as core_managers
from plans import models as plan_model


class User(AbstractUser):
    """
    Custom User Model
    기본으로 제공하는 장고 USER를 커스텀하여 유저 모델 생성
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

    hint_question = models.IntegerField(blank=False, default=1)
    hint = models.CharField(blank=False, max_length=200, default="")
    rating = models.IntegerField(default=10)

    objects = core_managers.CustomUserManager()

    def __str__(self):
        return self.first_name

    def delete(self, *args, **kargs):
        if self.avatar:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.file.path))
        super(User, self).delete(*args, **kargs)

    def get_rating(self):
        """
        사용자가 받은 피드백 점수를 합산하여
        사용자 정보를 계산한다.
        """
        rating = 0
        feedback_count = 0
        plans = plan_model.Plan.objects.filter(user=self.pk)

        for plan in plans:
            feedbacks = plan_model.Feedback.objects.filter(plan=plan)

            for feedback in feedbacks:
                rating += feedback.rating

            feedback_count += feedbacks.count()

        if feedback_count == 0:
            return 0
        return round(rating / feedback_count, 1)

    def get_avatar(self):
        """
        업로드된 이미지가 있을 경우 이미지 출력
        """
        if self.avatar:
            return self.avatar.url
        else:
            None

    def get_first_nickname(self):
        return self.first_name[0]
