# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext as _
from vanilla import CreateView, DeleteView, ListView, UpdateView, View
from inventory.forms import GroupForm
from inventory.models import Group, Photo

import logging
logger = logging.getLogger(__name__)

# Views for groups management

class ListGroups(LoginRequiredMixin, ListView):
    model = Group
    queryset = Group.objects.all().order_by('place')


class DeleteGroup(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('list_groups')


class CreateGroup(LoginRequiredMixin, View):
    template_name = 'inventory/group_form.html'

    def get(self, request):
        logging.debug('create group %s', request)
        return render(request, self.template_name, context={
            'form': GroupForm(),
        })

    def post(self, request):
        logging.debug('POST - create group')
        form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            logging.debug('saving group %s', group)
            if request.FILES:
                logger.debug(request.FILES)
                if 'group_upload' in request.FILES:
                    photo = Photo.objects.create(blob=request.FILES['group_upload'])
                    group.image = photo
            group.save()

            messages.add_message(request, messages.INFO, _("group_created"))
        else:
            print("valid error %s", form.errors)
            return render(request, self.template_name, context={'form': form, 'load_image':None})

        return redirect('list_groups')


class EditGroup(LoginRequiredMixin, View):
    template_name = 'inventory/group_form.html'

    def get(self, request, **kwargs):
        logging.info('GET - edit group' + kwargs['pk'])
        form = GroupForm()
        group = get_object_or_404(Group, pk=kwargs['pk'])
        form = GroupForm(instance=group)
        load_image = None

        if group.image:
            load_image = group.image
       
        return render(request, self.template_name, context={'form': form,  'load_image':load_image})

    def post(self, request, **kwargs):
        logger.debug("POST - edit group %s", request)
        group = get_object_or_404(Group, pk=kwargs['pk'])
        image = group.image
        form = GroupForm(data=request.POST, instance=group)
       
        if form.is_valid():
            logger.debug('form valid')
            pcd = form.cleaned_data
            group = form.save(commit=False)
            if request.FILES:
                logger.debug(request.FILES)
                if 'group_upload' in request.FILES:
                    photo = Photo.objects.create(blob=request.FILES['group_upload'])
                    group.image = photo
                    logger.debug('save image')
            else:
            	group.image = image

            group.save()

            messages.add_message(request, messages.INFO, _("group_edited"))

        else:
            return render(request, self.template_name,
                          context={'form': form, 'load_image': None})

        return redirect('list_groups')