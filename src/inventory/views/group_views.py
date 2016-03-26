# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from inventory.forms import GroupForm
from inventory.models import Group
from vanilla import CreateView, DeleteView, ListView, UpdateView


# Views for groups management

class ListGroups(ListView):
	model = Group
	queryset = Group.objects.all()


class CreateGroup(CreateView):
	model = Group
	form_class = GroupForm
	success_url = reverse_lazy('list_groups')


class EditGroup(UpdateView):
	model = Group
	form_class = GroupForm
	success_url = reverse_lazy('list_groups')


class DeleteGroup(DeleteView):
	model = Group
	success_url = reverse_lazy('list_groups')
