from django.contrib import admin
from . import models as plan_models

# Register your models here.


@admin.register(plan_models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "plan",
        "user",
        "title",
        "contents_for_plan",
    )


@admin.register(plan_models.PlanFile)
class PlanFileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "plan",
        "caption",
        "file",
    )


@admin.register(plan_models.ResultFile)
class ResultFileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "plan",
        "caption",
        "file",
    )


@admin.register(plan_models.Plan)
class PlanAdmin(admin.ModelAdmin):

    fieldsets = (
        ("Basic Info", {"fields": ("group", "user",)}),
        ("Plan Info", {"fields": ("title_for_plan", "contents_for_plan",)},),
        ("Result Info", {"fields": ("title_for_result", "contents_for_result",)},),
        ("Plan Setting", {"fields": ("start_day", "end_day", "status",)}),
    )

    list_display = (
        "id",
        "get_group_id",
        "group",
        "user",
        "title_for_plan",
        "contents_for_plan",
        "title_for_result",
        "contents_for_result",
        "start_day",
        "end_day",
        "status",
    )

    raw_id_fields = ("group", "user")
