from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models as user_models


@admin.register(user_models.User)
class UserAdmin(admin.ModelAdmin):

    USERADMIN_FIELDS = UserAdmin.fieldsets
    COSTOM_FIELDS = (
        ("CostomFields", {"fields": ("avatar", "gender", "rating", "login_method",)},),
    )

    fieldsets = USERADMIN_FIELDS + COSTOM_FIELDS

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "gender",
        "rating",
        "is_active",
        "login_method",
    )

    list_filter = UserAdmin.list_filter
