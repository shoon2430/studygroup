from django.shortcuts import render
from django.views.generic import FormView
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
        print(email, password)
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
        password = form.cleaned_data.get("password1")
        print(email, password)

        user = authenticate(self.request, username=email, password=password)
        print(user)
        if user is not None:
            print("succcess")
            login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


# def emailLogin(request):

#     if request.method == "POST":
#         form = loginForm(request.POST)
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(username=username, password=password)
#         print(user)

#     else:
#         form = loginForm()
#         return render(request, "users/user_login.html", {"form": form})
