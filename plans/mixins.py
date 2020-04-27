from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import reverse, redirect

from groups import models as group_models
from . import models as plan_models


class GroupRequiredMixin(LoginRequiredMixin):
    """
    그룹에 참여한 사람만 이용가능하도록 한다.
    """

    def dispatch(self, request, *args, **kwargs):
        dispatch = super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

        my = request.user
        group_pk = kwargs.get("group_pk")
        group = group_models.Group.objects.get(pk=group_pk)
        for user in group.users.all():
            if my == user:
                return dispatch

        messages.error(self.request, "그룹에 참여 후 가능합니다.")
        return redirect(reverse("groups:detail", args=(group_pk,)))


class PlanUserCheckMixin(LoginRequiredMixin):
    """
    자신의 계획인 경우만 이용가능하도록 한다.
    """

    def dispatch(self, request, *args, **kwargs):
        dispatch = super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

        my = request.user
        plan_pk = kwargs.get("plan_pk")
        plan = plan_models.Plan.objects.get(pk=plan_pk)

        if plan.user == my:
            return dispatch

        messages.error(self.request, "자신의 계획인 경우만 확인 가능합니다.")
        return redirect(reverse("groups:detail", args=(kwargs.get("group_pk"),)))
