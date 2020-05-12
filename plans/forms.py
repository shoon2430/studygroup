from datetime import datetime
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

    def clean_title_for_plan(self):
        title_for_plan = self.cleaned_data.get("title_for_plan")

        if title_for_plan == "":
            raise forms.ValidationError("필수 입력란 입니다.")

        return title_for_plan

    def clean_contents_for_plan(self):
        if self.cleaned_data.get("contents_for_plan") == "":
            raise forms.ValidationError("필수 입력란 입니다.")

        return self.cleaned_data.get("contents_for_plan")

    def save(self, *args, **kwargs):
        plan = super().save(commit=False)

        user = kwargs["user"]
        group = kwargs["group"]

        plan.user = user
        plan.group = group
        plan.save()


class updatePlanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(updatePlanForm, self).__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)

        if instance.status == "CONFIRM":
            self.fields["title_for_plan"].widget.attrs["readonly"] = True
            self.fields["contents_for_plan"].widget.attrs["readonly"] = True

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

    def clean_title_for_plan(self):
        title_for_plan = self.cleaned_data.get("title_for_plan")

        if title_for_plan == "":
            raise forms.ValidationError("필수 입력란 입니다.")

        return title_for_plan

    def clean_contents_for_plan(self):
        if self.cleaned_data.get("contents_for_plan") == "":
            raise forms.ValidationError("필수 입력란 입니다.")

        return self.cleaned_data.get("contents_for_plan")

    def save(self, *args, **kwargs):
        plan = super().save(commit=False)

        user = kwargs["user"]
        group = kwargs["group"]

        plan.user = user
        plan.group = group
        plan.save()


class planUploadForm(forms.ModelForm):
    class Meta:
        model = plan_models.PlanFile
        fields = [
            "file",
        ]

    def save(self, *args, **kwargs):
        planFile = super().save(commit=False)
        plan = kwargs["plan"]
        planFile.plan = plan
        return planFile


class resultUploadForm(forms.ModelForm):
    class Meta:
        model = plan_models.ResultFile
        fields = [
            "file",
        ]

    def save(self, *args, **kwargs):
        resultFile = super().save(commit=False)
        plan = kwargs["plan"]
        resultFile.plan = plan
        return resultFile


class creatFeedbackForm(forms.ModelForm):
    class Meta:
        model = plan_models.Feedback
        fields = [
            "title",
            "contents_for_plan",
            "rating",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "feedback title"}),
            "contents_for_plan": forms.Textarea(
                attrs={"placeholder": "feedback contents"}
            ),
            "rating": forms.TextInput(attrs={"hidden": "true"}),
        }

    def save(self, *args, **kwargs):
        feedback = super().save(commit=False)

        user = kwargs["user"]
        plan = kwargs["plan"]

        feedback.user = user
        feedback.plan = plan
        feedback.save()
