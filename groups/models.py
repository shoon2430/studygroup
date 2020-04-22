from datetime import datetime, timedelta
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

    WEEK_LIST = (
        ("MON", "월요일"),
        ("TUE", "화요일"),
        ("WHE", "수요일"),
        ("THU", "목요일"),
        ("FRI", "금요일"),
        ("SAT", "토요일"),
        ("SUN", "일요일"),
    )

    DAY_LIST = [(str(n), "{} 시".format(n)) for n in range(0, 24)]

    deadline_week = models.CharField(choices=WEEK_LIST, default="MON", max_length=5)
    deadline_day = models.CharField(choices=DAY_LIST, default=0, max_length=2)

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

    def get_weekday_idx(self):
        week_list = ("MON", "TUE", "WHE", "THU", "FRI", "SAT", "SUN")
        return week_list.index(self.deadline_week)
