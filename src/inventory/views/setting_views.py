# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext as _
from vanilla import CreateView, DeleteView, ListView, UpdateView, View
from inventory.forms import UserPreferenceForm
from inventory.models import UserPreference

import logging
logger = logging.getLogger(__name__)

# Views for UserPreference management

class ListUserPreferences(LoginRequiredMixin, ListView):
    model = UserPreference
    queryset = UserPreference.objects.all().order_by('id')


class DeleteUserPreference(LoginRequiredMixin, DeleteView):
    model = UserPreference
    success_url = reverse_lazy('list_userpreferences')


class EditUserPreference(LoginRequiredMixin, UpdateView):
    model = UserPreference
    form_class = UserPreferenceForm
    success_url = reverse_lazy('list_userpreferences')

    #def get_context_data(self, **kwargs):
    #    return super(EditUserPreference, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(data=request.POST, instance=self.object)

        if form.is_valid():
            self.object = form.save()
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())

        return self.form_invalid(form)