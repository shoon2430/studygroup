from django.contrib import admin
from . import models as group_models


@admin.register(group_models.Group)
class GroupAdmin(admin.ModelAdmin):

    fieldsets = (
        ("Basic Info", {"fields": ("title", "category", "notice", "contents",)},),
        ("Group Setting", {"fields": ("user", "max_group_count", "planning_unit")}),
    )

    list_display = (
        "id",
        "category",
        "title",
        "notice",
        "contents",
        "get_user_count",
        "max_group_count",
        "planning_unit",
        "created",
    )

    raw_id_fields = ("user",)

    ordering = ("id", "category")

    search_fields = ["id", "title"]
