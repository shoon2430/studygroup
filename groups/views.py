from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from . import models as group_model
from . import forms as group_form
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

        join = False

        for user in self.object.users.all():
            if user == self.request.user:
                join = True
        context["join"] = join

        return context


class createGroup(FormView):
    template_name = "groups/group_create.html"
    form_class = group_form.createGroupForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        leader = self.request.user
        form.save(user=leader)

        category = form.cleaned_data.get("category")
        title = form.cleaned_data.get("title")

        group = group_model.Group.objects.get(
            leader=leader, category=category, title=title
        )

        group.users.add(leader)

        return HttpResponseRedirect(self.get_success_url())


@csrf_exempt
def joinGroup(request, pk):

    if request.method == "POST":
        print(vars(request))

    return redirect(reverse("groups:detail", args=(pk,)))
