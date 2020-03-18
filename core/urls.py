from django.urls import path
from groups.views import GroupList

app_name = "core"

urlpatterns = [
    path("", GroupList.as_view(), name="home"),
]

