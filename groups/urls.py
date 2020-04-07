from django.urls import path
from . import views as group_views
from plans import views as plan_views

app_name = "groups"

urlpatterns = [
    path("create/", group_views.createGroup.as_view(), name="create-group"),
    path("<int:pk>/", group_views.GroupDetail.as_view(), name="detail"),
    path("<int:pk>/join/", group_views.joinGroup, name="join-group"),
    path("plan/<int:pk>", plan_views.PlanDetail.as_view(), name="plan-detail"),
]
