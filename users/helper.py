import re


def check_password(password1, password2, forms):

    if password1 != password2:
        raise forms.ValidationError("비밀번호가 동일하지 않습니다.")

    if len(password1) < 4 or len(password1) > 12:
        raise forms.ValidationError("비밀번호는 4자리 이상 12자리 이하입니다.")

    if re.findall("[a-zA-Z0-9]+", password1)[0] != password1:
        raise forms.ValidationError("비밀번호는 숫자와 영문자만 가능합니다.")
