from django.db import models
from core import models as core_model
from django.core.validators import MinValueValidator, MaxValueValidator


class Feedback(core_model.TimeStampModel):

    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=150)
    contents_for_plan = models.TextField(blank=False,)
    rating = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )


class PlanFile(core_model.TimeStampModel):
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)
    caption = models.CharField(max_length=150)
    file = models.FileField(null=True, upload_to="uploads/plan/file_for_plan")


class ResultFile(core_model.TimeStampModel):
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)
    caption = models.CharField(max_length=150)
    file = models.FileField(null=True, upload_to="uploads/plan/file_for_result")


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

    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    title_for_plan = models.CharField(blank=True, max_length=150)
    contents_for_plan = models.TextField(blank=True,)

    title_for_result = models.CharField(blank=True, max_length=150)
    contents_for_result = models.TextField(blank=True,)

    start_day = models.DateField(null=True, blank=True)
    end_day = models.DateField(null=True, blank=True)

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
        if next_status == "CONFIRM":
            self.status = "CONFIRM"
        elif next_status == "COMPLETE":
            self.status = "COMPLETE"
        elif next_status == "SUCCESS":
            self.status = "SUCCESS"

        self.save()
