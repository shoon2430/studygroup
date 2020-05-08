from django.db import models
from django.contrib.auth.models import UserManager


class CustomModelManager(models.Manager):
    """
    해당 모델객체를 가지고 오는지 확인
    ex) 
        User.objects.get(pk=pk) 했을 때 
        객체가 있을 경우만 리턴
        없는 경우 except

    """

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)

        except self.model.DoesNotExist:
            return None


class CustomUserManager(CustomModelManager, UserManager):
    """
    배포시 createsuperuser 명령을 위해 UserManager를 상속받음
    """

    pass
