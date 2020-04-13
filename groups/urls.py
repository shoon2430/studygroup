from django.urls import path
from . import views as group_views
from plans import views as plan_views

app_name = "groups"

urlpatterns = [
    path("create/", group_views.createGroup.as_view(), name="create-group"),
    path("mygroups/", group_views.MyGroupList.as_view(), name="my-groups"),
    path("<int:pk>/", group_views.GroupDetail.as_view(), name="detail"),
    path("<int:pk>/update/", group_views.updateGroup.as_view(), name="update-group"),
    path("<int:pk>/join/", group_views.join_or_exit_Group, name="join-group"),
    path(
        "<int:group_pk>/plan/<int:plan_pk>/",
        plan_views.PlanDetail.as_view(),
        name="plan-detail",
    ),
    path("<int:pk>/plan/create/", plan_views.createPlan.as_view(), name="plan-create"),
    path(
        "<int:group_pk>/plan/<int:plan_pk>/update/",
        plan_views.updatePlan.as_view(),
        name="plan-update",
    ),
    path(
        "<int:group_pk>/plan/<int:plan_pk>/delete/",
        plan_views.deletePlan,
        name="plan-delete",
    ),
    path(
        "<int:group_pk>/plan/<int:plan_pk>/confirm/",
        plan_views.confirmPlan,
        name="plan-confirm",
    ),
]
