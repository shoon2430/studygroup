from django.db import models


class TimeStampModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # 데이터베이스에 등록 x
    class Meta:
        abstract = True

    def get_created(self):
        return self.created.strftime("%Y %m %d %H %M %p")

    def get_updated(self):
        return self.updated.strftime("%Y %m %d %H %M %p")

    def get_created_kro(self):
        return self.created.strftime("%Y-%m-%d")
