# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from inventory.forms import GroupForm
from inventory.models import Group
from vanilla import CreateView, DeleteView, ListView, UpdateView


# Views for groups management

class ListGroups(LoginRequiredMixin, ListView):
	model = Group
	queryset = Group.objects.all()


class CreateGroup(LoginRequiredMixin, CreateView):
	model = Group
	form_class = GroupForm
	success_url = reverse_lazy('list_groups')


class EditGroup(LoginRequiredMixin, UpdateView):
	model = Group
	form_class = GroupForm
	success_url = reverse_lazy('list_groups')


class DeleteGroup(LoginRequiredMixin, DeleteView):
	model = Group
	success_url = reverse_lazy('list_groups')
