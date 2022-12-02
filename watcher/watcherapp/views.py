from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, status
from rest_framework.response import Response

from . import serializers
from .models import Active, Metrix, Email
from .forms import ActiveAddForm, ActiveEditForm, EmailAddForm, EmailDeleteForm
from .actives import ConectedActives, ActiveMetrix


error_405 = {'Error': '405 Method Not Allowed'}
error_403 = {'Error': '403 Forbidden'}

def in_group(user, group):
    return user.groups.filter(name=group).exists() 


class MetrixList(generics.CreateAPIView):
    serializer_class = serializers.MetrixSerializer

    def get(self, request, *args, **kwargs):
        token = request.headers.get('Active-Token')
        is_token = Active.objects.filter(active_token=token).exists()
        if not is_token:
            return Response(status=status.HTTP_403_FORBIDDEN, data=error_403)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data=error_405)

    def post(self, request, *args, **kwargs):
        token = request.headers.get('Active-Token')
        is_token = Active.objects.filter(active_token=token).exists()
        if not is_token:
            return Response(status=status.HTTP_403_FORBIDDEN, data=error_403)
        return self.create(request, *args, **kwargs)


class Index(TemplateView):
    template_name = 'index.html'


class ShowEmails(LoginRequiredMixin, View):
    template_name = 'show_emails.html'

    def get(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators"):
            emails_list_render = Email.objects.all()
            return render(request, 'show_emails.html', 
                        {'emails_list_render': emails_list_render})
        else:
            return HttpResponseRedirect('/')


class AddEmail(LoginRequiredMixin, FormView):
    template_name = 'add_email.html'
    form_class = EmailAddForm
    success_url = '/show/emails/'

    def get(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators"):
            return super(AddEmail, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def form_valid(self, form):
        if in_group(self.request.user, "administrators"):
            form.save()
            return super().form_valid(form)
        else:
            return HttpResponseRedirect('/')


class DeleteEmail(LoginRequiredMixin, DeleteView):
    model = Email
    template_name = 'delete_email.html'
    success_url = '/show/emails/'

    def get(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators"):
            return super(DeleteEmail, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def delete(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators"):
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseRedirect('/')


class AddActive(LoginRequiredMixin, FormView):
    template_name = 'add_active.html'
    form_class = ActiveAddForm
    success_url = '/show/actives/'

    def get(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators"):
            return super(AddActive, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def form_valid(self, form):
        if in_group(self.request.user, "administrators"):
            form.save()
            return super().form_valid(form)
        else:
            return HttpResponseRedirect('/')


class EditActive(LoginRequiredMixin, UpdateView):
    template_name = 'edit_active.html'
    form_class = ActiveEditForm
    success_url = '/show/actives/'

    def get(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators"):
            return super(EditActive, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def get_object(self):
        if in_group(self.request.user, "administrators"):
            pk = self.kwargs.get(self.pk_url_kwarg)
            return Active.objects.filter().get(pk=pk)
        else:
            return HttpResponseRedirect('/')


class DeleteActive(LoginRequiredMixin, DeleteView):
    model = Active
    template_name = 'delete_active.html'
    success_url = '/show/actives/'

    def get(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators"):
            return super(DeleteActive, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def delete(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators"):
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.object.delete()
            linked_metrix = Metrix.objects.filter(metrix_token=self.object.active_token)
            linked_metrix.delete()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseRedirect('/')


class ShowActive(LoginRequiredMixin, View):
    template_name = 'show_active_details.html'

    def get(self, request, *args, **kwargs):
        if in_group(self.request.user, "administrators") \
                    or in_group(self.request.user, "managers"):
            pk = self.kwargs.get('pk')
            metric_list_render = ActiveMetrix.get_metrix(pk)
            if metric_list_render == 1:
                return render(request, 'no_data_met.html')
            return render(request, 'show_active_details.html', 
                        {'metric_list_render': metric_list_render})
        else:
            return HttpResponseRedirect('/')


class ShowActives(LoginRequiredMixin, View):
    template_name = 'show_actives.html'

    def get(self, request):
        if in_group(self.request.user, "administrators") \
                    or in_group(self.request.user, "managers"):
            active_list_menu = ConectedActives.last_connected()
            active_list_render = ConectedActives.list_connected()
            if active_list_render == 1:
                return render(request, 'no_data_act.html')
            return render(request, 'show_actives.html', 
                        {'active_list_render': active_list_render, 
                        'active_list_menu': active_list_menu,})
        else:
            return HttpResponseRedirect('/')