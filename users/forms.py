
from django import forms
from . import models
from .helper import check_password


class loginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "ID"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("ID가 존재하지 않습니다."))

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return password
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀렸습니다."))
        except models.User.DoesNotExist:
            if self._errors.get("email") is None:
                self.add_error("email", forms.ValidationError("ID가 존재하지 않습니다."))


class signupForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["email", "first_name"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "닉네임"}),
            "email": forms.EmailInput(attrs={"placeholder": "아이디"}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )

    hint_question = forms.CharField(
        widget=forms.Select(
            choices=[(1, "당신의 고향은?"), (2, "어렸을때 별명은?"), (3, "현재 살고 있는 동네이름은?"),]
        )
    )
    hint = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "비밀번호 힌트"}))

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

        check_password(password1, password2, forms)
        return password1

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password1")
        hint_question = self.cleaned_data.get("hint_question")
        hint = self.cleaned_data.get("hint")

        user.username = email
        user.set_password(password)
        user.hint_question = hint_question
        user.hint = hint
        user.save()


class updateUserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["avatar", "first_name"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "닉네임"}),
        }

    def clean_first_name(self):
        """
        닉네임 중복확인
        """
        nickname = self.cleaned_data.get("first_name")
        
        if models.User.objects.filter(first_name=nickname):
            raise forms.ValidationError("사용중인 닉네임 입니다. 다른 이름으로 변경해주세요.")

        return nickname


class changePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "기존 비밀 번호를 입력 해주세요"})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "변경하실 비밀번호를 입력 해주세요"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "변경하실 비밀번호를 입력 해주세요"})
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")

        check_password(password1, password2, forms)
        return password1

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        password1 = self.cleaned_data.get("new_password1")

        if old_password == password1:
            raise forms.ValidationError("기존 비밀번호와 동일합니다.")
        return old_password


class findUserPasswordForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["email", "hint_question", "hint"]
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "ID"}),
            "hint_question": forms.Select(
                choices=[(1, "당신의 고향은?"), (2, "어렸을때 별명은?"), (3, "현재 살고 있는 동네이름은?")]
            ),
            "hint": forms.TextInput(attrs={"placeholder": "비밀번호 힌트"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("ID가 존재하지 않습니다."))

    def clean_hint(self):
        email = self.cleaned_data.get("email")
        hint_question = self.cleaned_data.get("hint_question")
        hint = self.cleaned_data.get("hint")

        try:
            user = models.User.objects.get(
                username=email, hint_question=hint_question, hint=hint
            )
            return hint
        except models.User.DoesNotExist:
            self.add_error("hint", forms.ValidationError("비밀번호 힌트가 틀렸습니다."))


class getUserNewPasswordForm(forms.Form):

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "변경하실 비밀번호를 입력 해주세요"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "변경하실 비밀번호를 입력 해주세요"})
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        check_password(password1, password2, forms)
        return password1
