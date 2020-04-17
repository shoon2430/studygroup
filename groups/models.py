from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core import models as core_model


class Group(core_model.TimeStampModel):

    CATEGORY_STUDY = "S"  # study
    CATEGORY_READING = "R"  # reading
    CATEGORY_EXERCISE = "E"  # exercise
    CATEGORY_HOBBY = "H"  # hobby

    CATEGORY_LIST = (
        (CATEGORY_STUDY, "Study"),
        (CATEGORY_READING, "Reading"),
        (CATEGORY_EXERCISE, "Exercise"),
        (CATEGORY_HOBBY, "Hobby"),
    )

    PLANNING_UNIT = (
        ("week", "Week"),
        ("day", "Day"),
    )

    leader = models.ForeignKey(
        "users.User", related_name="leader", on_delete=models.CASCADE
    )
    users = models.ManyToManyField("users.User", blank=True)
    category = models.CharField(
        choices=CATEGORY_LIST,
        default=CATEGORY_STUDY,
        blank=False,
        null=False,
        max_length=2,
    )
    title = models.CharField(blank=False, max_length=150)
    notice = models.TextField(blank=False,)
    contents = models.TextField(blank=False,)
    max_group_count = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    planning_unit = models.CharField(
        choices=PLANNING_UNIT, default="week", max_length=10, blank=False, null=False,
    )

    photo = models.ImageField(blank=True, upload_to="group/group_photo")

    def __str__(self):
        return self.title

    def get_user_count(self):
        return self.users.count()

    def get_photo(self):
        return self.photo.url

    def get_plan_count(self):
        return self.plans.filter(user=self.leader).count()

    def get_all_feedback_count(self):

        plans = self.plans.filter(user=self.leader)
        feedback_count = 0
        for plan in plans:
            feedback_count += plan.get_feedbacks()

        return feedback_count
