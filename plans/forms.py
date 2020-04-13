from django import forms
from . import models as plan_models


class createPlanForm(forms.ModelForm):
    class Meta:
        model = plan_models.Plan
        fields = [
            "title_for_plan",
            "contents_for_plan",
        ]

        widgets = {
            "title_for_plan": forms.TextInput(attrs={"placeholder": "title"}),
            "contents_for_plan": forms.Textarea(attrs={"placeholder": "contents"}),
        }

    def save(self, *args, **kwargs):
        plan = super().save(commit=False)

        user = kwargs["user"]
        group = kwargs["group"]

        plan.user = user
        plan.group = group
        plan.save()


class updatePlanForm(forms.ModelForm):
    class Meta:
        model = plan_models.Plan
        fields = [
            "title_for_plan",
            "contents_for_plan",
            "title_for_result",
            "contents_for_result",
        ]

        widgets = {
            "title_for_plan": forms.TextInput(attrs={"placeholder": "title"}),
            "contents_for_plan": forms.Textarea(attrs={"placeholder": "contents"}),
            "title_for_result": forms.TextInput(attrs={"placeholder": "result title"}),
            "contents_for_result": forms.Textarea(
                attrs={"placeholder": "result contents"}
            ),
        }

    def save(self, *args, **kwargs):
        plan = super().save(commit=False)

        user = kwargs["user"]
        group = kwargs["group"]

        plan.user = user
        plan.group = group
        plan.save()
