from django import forms
from . import models


class createGroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = [
            "photo",
            "category",
            "title",
            "notice",
            "contents",
            "max_group_count",
            "planning_unit",
            "deadline_week",
            "deadline_day",
        ]

        widgets = {
            "category": forms.Select(attrs={"placeholder": "category"}),
            "title": forms.TextInput(attrs={"placeholder": "title"}),
            "notice": forms.Textarea(attrs={"placeholder": "notice"}),
            "contents": forms.Textarea(attrs={"placeholder": "contents"}),
            "max_group_count": forms.TextInput(
                attrs={"placeholder": "max_group_count"}
            ),
        }

    def clean_max_group_count(self):
        max_group_count = self.cleaned_data.get("max_group_count")

        if max_group_count < 2 or max_group_count > 8:
            raise forms.ValidationError("최대그룹인원은 2~8명 입니다.")
        else:
            return max_group_count

    def save(self, *args, **kwargs):
        group = super().save(commit=False)

        group.max_group_count = self.cleaned_data.get("max_group_count")

        if group.planning_unit == "week":
            group.deadline_day = ""
        elif group.planning_unit == "day":
            group.deadline_week = ""

        user = kwargs["user"]
        group.leader = user
        group.save()


class updateGroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = [
            "photo",
            "category",
            "title",
            "notice",
            "contents",
            "max_group_count",
            "planning_unit",
            "deadline_week",
            "deadline_day",
        ]

        widgets = {
            "category": forms.Select(attrs={"placeholder": "category"}),
            "title": forms.TextInput(attrs={"placeholder": "title"}),
            "notice": forms.Textarea(attrs={"placeholder": "notice"}),
            "contents": forms.Textarea(attrs={"placeholder": "contents"}),
            "max_group_count": forms.TextInput(
                attrs={"placeholder": "max_group_count"}
            ),
        }

    def clean_max_group_count(self):
        max_group_count = self.cleaned_data.get("max_group_count")
        group = self.instance

        if max_group_count < 2 or max_group_count > 8:
            raise forms.ValidationError("최대그룹인원은 2~8명 입니다.")
        elif group.get_user_count() > max_group_count:
            raise forms.ValidationError("현재 그룹원 수 보다 적게 설정 할 수 없습니다.")
        else:
            return max_group_count
