from django.urls import path
from . import views

app_name = "groups"

urlpatterns = [
    path("<int:pk>/", views.GroupDetail.as_view(), name="detail"),
]

