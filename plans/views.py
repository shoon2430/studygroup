
from django.http import HttpResponseRedirect
from django.shortcuts import render ,reverse
from . import models as plan_models
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, CreateView

from .forms import createPlanForm

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
        print(pk, group)

        form.save(user=user, group=group)

        return HttpResponseRedirect(reverse("groups:detail", args=(pk,)))