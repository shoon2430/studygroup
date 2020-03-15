from django.db import models


class TimeStampModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # 데이터베이스에 등록 x
    class Meta:
        abstract = True
