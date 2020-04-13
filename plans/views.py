
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render ,reverse, redirect, get_object_or_404
from . import models as plan_models
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, CreateView, DeleteView, UpdateView

from .forms import createPlanForm, updatePlanForm

from groups import models as group_models
from . import models as plan_models


class PlanDetail(DetailView):
    model = plan_models.Plan

    def get_object(self, queryset=None):
        plan = plan_models.Plan.objects.get(pk=self.kwargs["plan_pk"])
        return plan


class createPlan(FormView):
    template_name = "plans/plan_create.html"
    form_class = createPlanForm
    success_url = reverse_lazy("core:home")


    def form_valid(self, form):
        
        user = self.request.user
        pk = self.kwargs['pk']
        
        group = group_models.Group.objects.get(pk=pk)
        form.save(user=user, group=group)

        return HttpResponseRedirect(reverse("groups:detail", args=(pk,)))

class updatePlan(UpdateView):
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
def deletePlan(request,group_pk, plan_pk):
    
    if request.method == "POST":
        try:
            plan_models.Plan.objects.get(pk=plan_pk).delete()
            return HttpResponseRedirect(reverse("groups:detail", args=(group_pk,)))

        except plan_models.Plan.DoesNotExist:
            return redirect(reverse('core:home'))


@csrf_exempt
def confirmPlan(request,group_pk, plan_pk):

    if request.method == "POST":
        try:
            myplan = plan_models.Plan.objects.get(pk=plan_pk)
            status = myplan.status
            
            if status == "ENROLLMENT":
                myplan.status = "CONFIRM"
            elif status == "COMPLETE":
                myplan.status = "SUCCESS"
            
            myplan.save()
            return HttpResponseRedirect(reverse("groups:plan-detail", args=(group_pk,plan_pk,))) 

        except plan_models.Plan.DoesNotExist:
            return redirect(reverse('core:home'))
