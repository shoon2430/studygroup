
import json

from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render ,reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import createPlanForm, updatePlanForm, creatFeedbackForm
from groups import models as group_models
from . import models as plan_models


class PlanDetail(LoginRequiredMixin, DetailView):
    model = plan_models.Plan

    def get_object(self, queryset=None):
        plan = plan_models.Plan.objects.get(pk=self.kwargs["plan_pk"])
        return plan


class createPlan(LoginRequiredMixin, FormView):
    '''
    Create Plan 
    '''
    template_name = "plans/plan_create.html"
    form_class = createPlanForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        
        user = self.request.user
        pk = self.kwargs['pk']
        
        group = group_models.Group.objects.get(pk=pk)
        form.save(user=user, group=group)

        return HttpResponseRedirect(reverse("groups:detail", args=(pk,)))


class updatePlan(LoginRequiredMixin, UpdateView):
    template_name = "plans/plan_update.html"
    form_class = updatePlanForm

    def get_object(self): 
        plan = get_object_or_404(plan_models.Plan, pk=self.kwargs['plan_pk'])
        return plan
    
    def form_valid(self, form):
        
        user = self.request.user
        pk = self.kwargs['group_pk']
        
        group = group_models.Group.objects.get(pk=pk)
        form.save(user=user, group=group)

        return HttpResponseRedirect(reverse("groups:detail", args=(pk,)))


@csrf_exempt
@login_required
def deletePlan(request, group_pk, plan_pk):
    
    if request.method == "POST":
        try:
            plan_models.Plan.objects.get(pk=plan_pk).delete()
            return HttpResponseRedirect(reverse("groups:detail", args=(group_pk,)))

        except plan_models.Plan.DoesNotExist:
            return redirect(reverse('core:home'))


@csrf_exempt
@login_required
def change_plan_status(request, group_pk, plan_pk):

    if request.method == "POST":
        try:
            myplan = plan_models.Plan.objects.get(pk=plan_pk)

            next_status = json.loads(request.body.decode("utf-8")).get("next_status")
            myplan.set_status_change(next_status)

            # if next_status == "CONFIRM":
            return HttpResponseRedirect(reverse("groups:plan-detail", args=(group_pk,plan_pk,))) 
            # else :
            #     return redirect(reverse('groups:plan-update', args=(group_pk,plan_pk,)))

        except plan_models.Plan.DoesNotExist:
            return redirect(reverse('core:home'))


class createFeedback(LoginRequiredMixin, FormView):
    template_name = "feedbacks/feedback_create.html"
    form_class = creatFeedbackForm
    
    def form_valid(self, form):
        
        user = self.request.user

        group_pk = self.kwargs['group_pk']
        plan_pk = self.kwargs['plan_pk']

        plan = plan_models.Plan.objects.get(pk=plan_pk)
        plan.set_status_change("SUCCESS")
        plan.save()
        form.save(user=user, plan=plan)

        return HttpResponseRedirect(reverse("groups:plan-detail", args=(group_pk,plan_pk,))) 
        