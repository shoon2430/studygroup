from django.urls import path
from . import views as plan_views

app_name = "plans"

urlpatterns = [
    path("", plan_views.PlanList.as_view(), name="plan-list"),
    # path("feedbacks/", plan_views.FeedbackList.as_view(), name="feedback-list"),
    path(
        "feedbacks/<int:pk>",
        plan_views.FeedbackDetail.as_view(),
        name="feedback-detail",
    ),
]
