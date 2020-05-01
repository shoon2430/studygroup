from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/kakao", views.kakago_get_token, name="kakao-token"),
    path("login/kakao/callback", views.kakaoLogin, name="kakao-login"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.signupView.as_view(), name="signup"),
    path("<int:pk>/info/", views.userInfromationView.as_view(), name="info"),
]
