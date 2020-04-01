from django import forms
from . import models


class loginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("Email does not exist"))

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print(email,password)
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                self.add_error(None, forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class signupForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First_name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last_name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password1"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password2"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        user = models.User.objects.filter(email=email)
        if user:
            raise forms.ValidationError("이미 존재하는 아이디 입니다.")
        else:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 == password2:
            return password1

        else:
            raise forms.ValidationError("비밀번호가 동일하지 않습니다.")

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")

        user.username = email
        user.set_password(password)
        user.save()
