from django.shortcuts import render
from . import models as plan_models
from django.views.generic import DetailView


# Create your views here.


class PlanDetail(DetailView):
    model = plan_models.Plan

