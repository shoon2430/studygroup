import os
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import FormView, DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import User
from .forms import loginForm, signupForm, updateUserForm, changePasswordForm


class LoginView(FormView):
    """
    사용자 로그인
    """

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
    """
    사용자 로그아웃
    """
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
    """
    사용자 정보 조회
    """

    model = User


class userUpdateView(LoginRequiredMixin, UpdateView):
    """
    사용자 정보 변경
    """

    model = User
    template_name = "users/user_update_form.html"
    form_class = updateUserForm

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse_lazy("user:info", args=(self.request.user.pk,))


class userChangePasswordView(LoginRequiredMixin, FormView):
    """
    사용자 비밀번호 변경
    """

    model = User
    template_name = "users/user_update_password_form.html"
    form_class = changePasswordForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        user = self.request.user
        old_password = form.cleaned_data.get("old_password")

        if check_password(old_password, user.password):
            new_password = form.cleaned_data.get("new_password1")
            user.set_password(new_password)
            user.save()

            messages.info(self.request, "비밀번호가 변경되었습니다. 변경된 비밀번호로 로그인해주세요")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, "기존 비밀번호가 동일하지 않습니다.")
            return HttpResponseRedirect(reverse("user:password", args=(user.pk,)))
