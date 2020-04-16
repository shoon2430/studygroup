from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView
from . import models as group_model
from . import forms as group_form
from plans import models as plan_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class GroupList(ListView):
    model = group_model.Group
    context_object_name = "groups"
    paginate_by = "10"
    paginate_orphans = "5"
    ordering = "-created"


class GroupDetail(LoginRequiredMixin, DetailView):
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


class createGroup(LoginRequiredMixin, FormView):
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


class updateGroup(LoginRequiredMixin, UpdateView):
    model = group_model.Group
    template_name = "groups/group_update.html"
    form_class = group_form.updateGroupForm
    success_url = reverse_lazy("core:home")


@csrf_exempt
@login_required
def join_or_exit_Group(request, pk):

    if request.method == "POST":
        if request.user.is_authenticated:
            group = group_model.Group.objects.get(pk=pk)

            for user in group.users.all():
                if user == request.user:

                    plan_model.Plan.objects.filter(group=group, user=user).delete()
                    group.users.remove(request.user)
                    return HttpResponseRedirect(reverse("core:home"))

            group.users.add(request.user)
            return HttpResponseRedirect(reverse("groups:detail", args=(pk,)))
        else:
            next_url = reverse("groups:detail", args=(pk,))
            return HttpResponseRedirect(reverse("user:login") + "?next=" + next_url)


class MyGroupList(LoginRequiredMixin, ListView):
    model = group_model.Group
    template_name = "groups/mygroup_list.html"
    context_object_name = "groups"
    paginate_by = "10"
    paginate_orphans = "5"
    ordering = "-created"

    def get_queryset(self):
        qs_groups = super(MyGroupList, self).get_queryset()
        my = self.request.user
        qs_groups = qs_groups.filter(users=my)

        pk = self.request.GET.get("leader")

        if pk and pk == str(my.pk):
            qs_groups = qs_groups.filter(leader=my)
        return qs_groups
