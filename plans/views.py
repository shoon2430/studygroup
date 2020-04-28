import os
import json
from django.conf import settings
from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    createPlanForm,
    updatePlanForm,
    creatFeedbackForm,
    planUploadForm,
    resultUploadForm,
)
from groups import models as group_models
from . import models as plan_models

from .mixins import GroupRequiredMixin, PlanUserCheckMixin


class PlanDetail(GroupRequiredMixin, DetailView):
    model = plan_models.Plan

    def get_object(self, queryset=None):
        plan = plan_models.Plan.objects.get(pk=self.kwargs["plan_pk"])
        return plan


class createPlan(LoginRequiredMixin, FormView):

    template_name = "plans/plan_create.html"
    form_class = createPlanForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        user = self.request.user
        pk = self.kwargs["pk"]

        group = group_models.Group.objects.get(pk=pk)
        form.save(user=user, group=group)

        return HttpResponseRedirect(reverse("groups:detail", args=(pk,)))


class updatePlan(LoginRequiredMixin, UpdateView):
    template_name = "plans/plan_update.html"
    form_class = updatePlanForm

    def get_object(self):
        plan = get_object_or_404(plan_models.Plan, pk=self.kwargs["plan_pk"])
        return plan

    def form_valid(self, form):

        user = self.request.user
        group_pk = self.kwargs["group_pk"]
        plan_pk = self.kwargs["plan_pk"]

        group = group_models.Group.objects.get(pk=group_pk)
        form.save(user=user, group=group)

        next_status = self.request.POST.get("next_status")
        if next_status:
            plan = get_object_or_404(plan_models.Plan, pk=plan_pk)
            plan.set_status_change(next_status)
            plan.save()

        return HttpResponseRedirect(
            reverse("groups:plan-detail", args=(group_pk, plan_pk,))
        )


@csrf_exempt
@login_required
def deletePlan(request, group_pk, plan_pk):

    if request.method == "POST":
        try:
            print("WERWER")
            plan_models.Plan.objects.get(pk=plan_pk).delete()
            return HttpResponseRedirect(reverse("groups:detail", args=(group_pk,)))

        except plan_models.Plan.DoesNotExist:
            return redirect(reverse("core:home"))


@csrf_exempt
@login_required
def change_plan_status(request, group_pk, plan_pk):
    """
    계획 승인 절차
    ENROLLMENT -> CONFIRM -> COMPLETE -> SUCCESS
    """
    if request.method == "POST":
        try:
            plan = plan_models.Plan.objects.get(pk=plan_pk)
            next_status = json.loads(request.body.decode("utf-8")).get("next_status")

            plan.set_status_change(next_status)
            plan.save()

            return redirect(reverse("groups:plan-detail", args=(group_pk, plan_pk,)))

        except plan_models.Plan.DoesNotExist:
            return redirect(reverse("core:home"))


class plan_upload(FormView):
    """
    계획 등록시 파일 업로드
    """

    form_class = planUploadForm
    template_name = "plans/plan_upload.html"

    def form_valid(self, form):

        group_pk = self.kwargs["group_pk"]
        plan_pk = self.kwargs["plan_pk"]
        plan = plan_models.Plan.objects.get(pk=plan_pk)

        planFile = form.save(plan=plan)
        planFile.caption = self.request.FILES["file"].name
        planFile.save()

        return HttpResponseRedirect(
            reverse("groups:plan-detail", args=(group_pk, plan_pk,))
        )


class result_upload(FormView):
    """
    계획 완료시 파일 업로드
    """

    form_class = resultUploadForm
    template_name = "plans/result_upload.html"

    def form_valid(self, form):

        group_pk = self.kwargs["group_pk"]
        plan_pk = self.kwargs["plan_pk"]
        file_for_plan = plan_models.Plan.objects.get(pk=plan_pk)

        resultFile = form.save(plan=file_for_plan)

        resultFile.caption = self.request.FILES["file"].name
        resultFile.save()

        return HttpResponseRedirect(
            reverse("groups:plan-update", args=(group_pk, plan_pk,))
        )


class createFeedback(LoginRequiredMixin, FormView):
    template_name = "feedbacks/feedback_create.html"
    form_class = creatFeedbackForm

    def form_valid(self, form):
        user = self.request.user

        group_pk = self.kwargs["group_pk"]
        plan_pk = self.kwargs["plan_pk"]
        plan = plan_models.Plan.objects.get(pk=plan_pk)
        plan.set_status_change("SUCCESS")
        plan.save()
        form.save(user=user, plan=plan)

        return HttpResponseRedirect(
            reverse("groups:plan-detail", args=(group_pk, plan_pk,))
        )


class PlanList(LoginRequiredMixin, ListView):
    """
    나의 그룹 보기에서 선택 가능한 그룹리스트 보기
    내가 속한 그룹에서 내가 작성한 계획 전부를 조회한다.
    """

    model = plan_models.Plan
    context_object_name = "plans"
    paginate_by = "10"
    paginate_orphans = "5"
    ordering = ["-created"]
    template_name = "plans/plan_list.html"

    def get_queryset(self):
        queryset = super(PlanList, self).get_queryset()
        group_pk = self.request.GET.get("group")
        group = group_models.Group.objects.get(pk=group_pk)
        user = self.request.user
        queryset = queryset.filter(user=user, group=group)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PlanList, self).get_context_data(**kwargs)
        group = group_models.Group.objects.get(pk=self.request.GET.get("group"))
        context["group"] = group
        return context


class FeedbackList(PlanUserCheckMixin, ListView):
    """
    그룹 정보화면에서 선택 할 수 있는 피드백 리스트
    내가 작성한 하나의 계획에 대한 모든 피드백을 조회한다.
    """

    model = plan_models.Feedback
    context_object_name = "feedbacks"
    paginate_by = "10"
    paginate_orphans = "5"
    ordering = ["-plan__created", "-created"]
    template_name = "feedbacks/feedback_list.html"

    def get_queryset(self):
        queryset = super(FeedbackList, self).get_queryset()
        plan_pk = self.kwargs["plan_pk"]
        plan = plan_models.Plan.objects.get(pk=plan_pk)

        queryset = queryset.filter(plan=plan)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(FeedbackList, self).get_context_data(**kwargs)
        plan_pk = self.kwargs["plan_pk"]
        plan = plan_models.Plan.objects.get(pk=plan_pk)
        context["plan"] = plan
        return context


class MyFeedbackList(LoginRequiredMixin, ListView):
    """
    나의 그룹 보기 에서 선택 할 수 있는 피드백 리스트
    내가 속한 그룹에서 작성한 모든 계획에 대한 피드백을 조회한다. 
    """

    model = plan_models.Feedback
    context_object_name = "feedbacks"
    paginate_by = "10"
    paginate_orphans = "5"
    ordering = ["-plan__created", "-created"]
    template_name = "feedbacks/myfeedback_list.html"

    def get_queryset(self):
        queryset = super(MyFeedbackList, self).get_queryset()
        user = self.request.user
        group_pk = self.request.GET.get("group")

        queryset = queryset.filter(plan__group=group_pk, plan__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyFeedbackList, self).get_context_data(**kwargs)
        user = self.request.user
        group_pk = self.request.GET.get("group")
        group = group_models.Group.objects.get(pk=group_pk)

        plans = set()
        for plan in group.plans.all():
            if plan.user == user:
                Feedbacks = plan_models.Feedback.objects.filter(plan=plan)
                if Feedbacks:
                    plans.add(plan)

        context["plans"] = plans
        return context


class FeedbackDetail(LoginRequiredMixin, DetailView):
    model = plan_models.Feedback
    template_name = "feedbacks/feedback_detail.html"
