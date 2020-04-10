from django import forms
from . import models as plan_models


class createPlanForm(forms.ModelForm):
    class Meta:
        model = plan_models.Plan
        fields = [
            "title_for_plan",
            "contents_for_plan",
            # "start_day",
            # "end_day",
        ]

        widgets = {
            "title_for_plan": forms.TextInput(attrs={"placeholder": "title"}),
            "contents_for_plan": forms.Textarea(attrs={"placeholder": "contents"}),
            # "start_day": forms.DateTimeInput(),
            # "end_day": forms.DateTimeInput(),
        }

    def save(self, *args, **kwargs):
        print("HHIHIHIHIIs")
        plan = super().save(commit=False)

        user = kwargs["user"]
        group = kwargs["group"]
        print("=====sf=sdf=sf===")
        print(user, group)

        plan.user = user
        plan.group = group
        plan.save()
