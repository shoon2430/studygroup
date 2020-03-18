from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models as group_model
from plans import models as plan_model


class GroupList(ListView):
    model = group_model.Group
    context_object_name = "groups"
    paginate_by = "10"
    paginate_orphans = "5"
    ordering = "created"


class GroupDetail(DetailView):
    model = group_model.Group

    def get_context_data(self, **kwargs):
        context = super(GroupDetail, self).get_context_data(**kwargs)
        context["plans"] = plan_model.Plan.objects.filter(group=self.object).order_by(
            "-created"
        )
        return context
