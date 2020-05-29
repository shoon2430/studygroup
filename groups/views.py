from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.template.loader import render_to_string

from . import models as group_model
from . import forms as group_form
from plans import models as plan_model


class GroupList(ListView):
    model = group_model.Group
    context_object_name = "groups"
    paginate_by = "10"
    paginate_orphans = "2"
    ordering = "-created"

    def get_queryset(self):
        """
        조회 조건이 존재할 경우 필터링하여 리스트를 조회한다.
        """
        queryset = super(GroupList, self).get_queryset()
        title = self.request.GET.get("title")
        category = self.request.GET.get("category")

        if title:
            queryset = queryset.filter(title__contains=str(title))
        if category:
            queryset = queryset.filter(category=str(category))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupList, self).get_context_data(**kwargs)

        title = self.request.GET.get("title")
        category = self.request.GET.get("category")

        context["title"] = title
        context["category"] = category

        return context


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


@csrf_exempt
@login_required
def deleteGroup(request, pk):
    if request.method == "POST":

        group_model.Group.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse("core:home"))

    return HttpResponseRedirect(reverse("core:home"))


class updateGroup(LoginRequiredMixin, UpdateView):
    model = group_model.Group
    template_name = "groups/group_update.html"
    form_class = group_form.updateGroupForm
    success_url = reverse_lazy("core:home")


@csrf_exempt
@login_required
def join_or_exit_Group(request, pk):
    """
    해당 그룹에 속해있는지 확인
    
    그룹에 속해 있으면 그룹 나가기
    그룹에 속해 있지 않으면 그룹 참여
    """
    if request.method == "POST":
        group = group_model.Group.objects.get(pk=pk)

        for user in group.users.all():
            if user == request.user:
                if len(group.users.all()) == 1:
                    group.delete()

                    return HttpResponseRedirect(reverse("core:home"))

                plan_model.Plan.objects.filter(group=group, user=user).delete()
                group.users.remove(request.user)
                return HttpResponseRedirect(reverse("core:home"))

        group.users.add(request.user)
        return HttpResponseRedirect(reverse("groups:detail", args=(pk,)))


class MyGroupList(LoginRequiredMixin, ListView):
    """
    나의 그룹 보기
    내가 속한 그룹들만 조회하도록 한다.
    """

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
        return qs_groups
