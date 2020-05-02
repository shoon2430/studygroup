import os
import requests
from django.shortcuts import render
from django.views.generic import FormView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
from .models import User
from .forms import loginForm, signupForm


class LoginView(FormView):

    template_name = "users/user_login.html"
    form_class = loginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse_lazy("core:home")


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class signupView(FormView):
    template_name = "users/user_signup.html"
    form_class = signupForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password2")

        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class userInfromationView(DetailView):
    model = User


def kakago_get_token(request):
    app_key = os.environ.get("KAKAGO_REST_API_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    URL = f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"

    return redirect(URL)


class KakaoException(Exception):
    pass


def kakaoLogin(request):
    try:
        code = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id="
        )
    except KakaoException:
        return redirect(reverse("users:login"))



def kakao_callback(request):
    try:
        app_key = os.environ.get("KAKAO_REST_API")
        redirect_uri = "http://localhost:8000/user/continue/kakao/callback"
        code = request.GET.get("code")
        if code is not None:
            token_request = requests.post(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_key}&redirect_uri={redirect_uri}&code={code}&"
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise KakacoException("Can't get authorization code.")

            access_token = token_json.get("access_token")
            profile_request = requests.get(
                f"https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            email = profile_json.get("kakao_account").get("email", None)

            if email is not None:
                properties = profile_json.get("properties")
                nickname = properties.get("nickname", "I don't have Nickname")
                profile_image = properties.get("profile_image")
                nickname = "hoon"
                try:
                    user = models.User.objects.get(email=email)
                    if user.login_method != models.User.LOGIN_KAKAO:
                        raise KakacoException(
                            f"Please log in with : {user.login_method}"
                        )

                except models.User.DoesNotExist:
                    user = models.User.objects.create(
                        email=email,
                        username=email,
                        first_name=nickname,
                        login_method=models.User.LOGIN_KAKAO,
                        email_verified=True,
                    )
                    user.set_unusable_password()
                    user.save()
                    if profile_image is not None:
                        photo_request = requests.get(profile_image)
                        user.avatar.save(
                            f"{nickname}-avatar", ContentFile(photo_request.content)
                        )

                login(request, user)
                messages.success(request, f"Welcome back {user.first_name}")
                return redirect(reverse("core:home"))
            else:
                raise KakacoException("Can't get your profile")
        else:
            raise KakacoException("Can't get code")
    except KakacoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))
