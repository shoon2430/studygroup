import os
from django.conf import settings
from datetime import datetime, timedelta
from django.db import models
from core import models as core_model
from django.core.validators import MinValueValidator, MaxValueValidator


class Feedback(core_model.TimeStampModel):

    plan = models.ForeignKey("Plan", related_name="feedbacks", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=150)
    contents_for_plan = models.TextField(blank=False,)
    rating = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def star_count(self):
        return range(0, self.rating)

    def none_star_count(self):
        return range(0, 5 - self.rating)


class PlanFile(core_model.TimeStampModel):
    plan = models.ForeignKey("Plan", related_name="planfiles", on_delete=models.CASCADE)
    caption = models.CharField(max_length=150)
    file = models.FileField(null=True, upload_to="plan/file_for_plan")

    def delete(self, *args, **kargs):
        if self.file:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.file.path))
        super(PlanFile, self).delete(*args, **kargs)


class ResultFile(core_model.TimeStampModel):
    plan = models.ForeignKey(
        "Plan", related_name="resultfiles", on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=150)
    file = models.FileField(null=True, upload_to="plan/file_for_result")

    def delete(self, *args, **kargs):
        if self.file:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.file.path))
        super(ResultFile, self).delete(*args, **kargs)


class Plan(core_model.TimeStampModel):

    STATUS_ENROLLMENT = "ENROLLMENT"
    STATUS_CONFIRM = "CONFIRM"
    STATUS_COMPLETE = "COMPLETE"
    STATUS_SUCCESS = "SUCCESS"

    STATUS_LIST = (
        (STATUS_ENROLLMENT, "Enrollment"),
        (STATUS_CONFIRM, "Confirm"),
        (STATUS_COMPLETE, "Complete"),
        (STATUS_SUCCESS, "Success"),
    )

    group = models.ForeignKey(
        "groups.Group", related_name="plans", on_delete=models.CASCADE
    )
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    title_for_plan = models.CharField(blank=True, max_length=150)
    contents_for_plan = models.TextField(blank=True,)

    title_for_result = models.CharField(blank=True, max_length=150)
    contents_for_result = models.TextField(blank=True,)

    deadline = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        choices=STATUS_LIST,
        default=STATUS_ENROLLMENT,
        blank=False,
        null=False,
        max_length=20,
    )

    def __str__(self):
        plan_id = str(self.id).zfill(8)
        return f"PLAN_{plan_id}"

    def get_group_id(self):
        return self.group.id

    def set_status_change(self, next_status):
        self.status = next_status

    def cal_week_deadline(self, enrollment_date, std_weekday):
        """
        주간 계획 마감일자 계산
        
        마감일까지 일주일보다 적게 걸리는 경우
        마감날짜 = 마감일까지의 기간 + 일주일
        """
        weekday = enrollment_date.weekday()
        if std_weekday > weekday:
            between_day = std_weekday - weekday
            add_day = timedelta(days=(between_day + 7))

        else:
            between_day = std_weekday - weekday
            add_day = timedelta(days=(7 - between_day))

        deadline = enrollment_date + add_day
        deadline = deadline.replace(hour=0, minute=0, second=0)
        return deadline

    def cal_day_deadline(self, today, hour):
        """
        일간 계획 마감일자 계산

        마감시간까지 24시간 보다 적게 걸리는 경우
        마감시간 = 다음날 마감시간까지
        """

        if today.hour < int(hour):
            add_day = timedelta(days=(2))
        else:
            add_day = timedelta(days=(1))

        deadline = today + add_day
        deadline = deadline.replace(hour=int(hour), minute=0, second=0)
        return deadline

    def get_feedbacks(self):
        return self.feedbacks.count()

    def get_planFiles(self):
        planfiles = self.planfiles.all()
        return planfiles

    def get_resultfiles(self):
        resultfiles = self.resultfiles.all()
        return resultfiles

    def get_deadline(self):
        if self.deadline:
            return self.deadline.strftime("%Y %m %d %H %M %p")
        else:
            return ""

    def check_deadline(self):
        """
        마감기간이 마감 되었는지 확인
        """
        if self.deadline:
            now = datetime.now()
            deadline = self.deadline
            return now > deadline
        else:
            return False
