from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.signupView.as_view(), name="signup"),
    path("<int:pk>/info/", views.userInfromationView.as_view(), name="info"),
    path(
        "<int:pk>/info/password/",
        views.userChangePasswordView.as_view(),
        name="password",
    ),
    path("<int:pk>/info/update/", views.userUpdateView.as_view(), name="update"),
]
