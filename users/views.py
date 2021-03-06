from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import User
from .forms import (
    loginForm,
    signupForm,
    updateUserForm,
    changePasswordForm,
    findUserPasswordForm,
    getUserNewPasswordForm,
)


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


class userInfromationView(LoginRequiredMixin, DetailView):
    """
    사용자 정보 조회
    """

    model = User


class userUpdateView(LoginRequiredMixin, UpdateView):
    """
    사용자 정보 변경
    사용자 정보는 프로필 사진과 닉네임을 변경 할 수 있다.
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

            messages.success(self.request, "비밀번호가 변경되었습니다. 변경된 비밀번호로 로그인해주세요")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, "기존 비밀번호가 동일하지 않습니다.")
            return HttpResponseRedirect(reverse("user:password", args=(user.pk,)))


class findUserPasswordView(FormView):
    """
    사용자 비밀번호 찾기
    비밀번호 찾기는 회원가입시에 입력한 힌트를 이용해서 찾을 수 있다.
    """

    model = User
    template_name = "users/user_find_password.html"
    form_class = findUserPasswordForm
    success_url = reverse_lazy("user:findpassword")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        hint_question = form.cleaned_data.get("hint_question")
        hint = form.cleaned_data.get("hint")

        # 비밀번호 찾기 힌트가 맞는지 확인
        user = User.objects.filter(
            username=email, hint_question=hint_question, hint=hint
        )[0]
        if user:
            # 힌트가 맞을경우 세션에 추가하여 인증 유지
            self.request.session["auth"] = user.username
            return redirect(reverse("user:getNewPassword"))

        return HttpResponseRedirect(self.get_success_url())


class getUserNewPasswordView(FormView):
    """
    비밀번호 찾기 인증 성공시 새로운 비밀번호를 발급받는 화면 호출
    """

    model = User
    template_name = "users/user_get_newpassword.html"
    form_class = getUserNewPasswordForm
    success_url = reverse_lazy("user:login")

    def form_valid(self, form):

        if not self.request.session.get("auth", False):
            messages.error(self.request, "인증되지 않았습니다.")
            return HttpResponseRedirect(self.get_success_url())

        try:
            # 인증된 유저정보를 가지고와서 비밀번호 변경 시작
            user = User.objects.get(username=self.request.session["auth"])
            new_password = form.cleaned_data.get("new_password1")
            user.set_password(new_password)
            user.save()

            messages.success(self.request, "비밀번호가 변경되었습니다. 로그인하세요.")
            logout(self.request)
            return HttpResponseRedirect(self.get_success_url())

        except User.DoesNotExist:
            logout(self.request)
            return HttpResponseRedirect(self.get_success_url())
