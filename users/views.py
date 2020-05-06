import os
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
from .models import User
from .forms import loginForm, signupForm, updateUserForm


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


class userUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/user_update_form.html"
    form_class = updateUserForm

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse_lazy("user:info", args=(self.request.user.pk,))


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
