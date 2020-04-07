from django import forms
from . import models


class createGroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = [
            "category",
            "title",
            "notice",
            "contents",
            "max_group_count",
            "planning_unit",
        ]

        widgets = {
            "category": forms.Select(attrs={"placeholder": "category"}),
            "title": forms.TextInput(attrs={"placeholder": "title"}),
            "notice": forms.Textarea(attrs={"placeholder": "notice"}),
            "contents": forms.Textarea(attrs={"placeholder": "contents"}),
            "max_group_count": forms.TextInput(
                attrs={"placeholder": "max_group_count"}
            ),
            "planning_unit": forms.Select(attrs={"placeholder": "planning_unit"}),
        }

    def save(self, *args, **kwargs):
        group = super().save(commit=False)
        user = kwargs["user"]
        group.leader = user
        group.save()
