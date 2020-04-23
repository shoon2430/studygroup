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


class PlanFile(core_model.TimeStampModel):
    plan = models.ForeignKey("Plan", related_name="planfiles", on_delete=models.CASCADE)
    caption = models.CharField(max_length=150)
    file = models.FileField(null=True, upload_to="plan/file_for_plan")


class ResultFile(core_model.TimeStampModel):
    plan = models.ForeignKey(
        "Plan", related_name="resultfiles", on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=150)
    file = models.FileField(null=True, upload_to="plan/file_for_result")


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
        """
        계획 CONFIRM시 마감일자 계산
        week 일 경우와 day 일 경우를 나누어 계산한다.
        """
        if next_status == "CONFIRM":
            enrollment_date = self.created

            if self.group.planning_unit == "week":
                deadline = self.cal_week_deadline(
                    enrollment_date, self.group.get_weekday_idx()
                )
                self.deadline = deadline

            elif self.group.planning_unit == "day":
                hour = self.group.deadline_day
                deadline = self.cal_day_deadline(enrollment_date, hour)
                self.deadline = deadline

        self.status = next_status

    def cal_week_deadline(self, enrollment_date, std_weekday):
        """
        주간 계획 마감일자 계산
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
        마감일보다 이후면 마감 
        """
        now = datetime.now()
        deadline = self.deadline

        return now > deadline
