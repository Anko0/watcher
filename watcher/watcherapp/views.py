from rest_framework import generics

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.views import View

from . import serializers
from .models import Active, Metrix
from .forms import ActiveForm, ActiveEditForm


class ActiveList(generics.ListCreateAPIView):
    queryset = Active.objects.all()
    serializer_class = serializers.ActiveSerializer


class ActiveDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Active.objects.all()
    serializer_class = serializers.ActiveSerializer


class MetrixList(generics.ListCreateAPIView):
    queryset = Metrix.objects.all()
    serializer_class = serializers.MetrixSerializer


class MetrixDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Metrix.objects.all()
    serializer_class = serializers.MetrixSerializer


class Index(TemplateView):
    template_name = 'index.html'


class AddActive(FormView):
    template_name = 'add_active.html'
    form_class = ActiveForm
    success_url = '/show/actives/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EditActive(UpdateView):
    template_name = 'edit_active.html'
    form_class = ActiveEditForm
    success_url = '/show/actives/'

    def get_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Active.objects.filter().get(pk=pk)


class DeleteActive(DeleteView):
    model = Active
    template_name = 'delete_active.html'
    success_url = '/show/actives/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        linked_metrix = Metrix.objects.filter(metrix_token=self.object.active_token)
        linked_metrix.delete()
        return HttpResponseRedirect(success_url)


class ShowActive(View):
    template_name = 'show_active_details.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.object = Active.objects.filter().get(pk=pk)
        metric_list = Metrix.objects.filter(metrix_token=self.object.active_token) \
                                    .latest('metrix_created')
        metric_list_5 = Metrix.objects.filter(metrix_token=self.object.active_token) \
                                      .order_by('-metrix_created')[:15][::-1] 
                                      #fix it to partitional select

        active_hostname = self.object.active_hostname
        if active_hostname != metric_list.metrix_uname['hostname'][0]:
            active_hostname = "%s is wrong! Real hostname is %s" % \
                              (active_hostname, metric_list.metrix_uname['hostname'][0])
        active_ip = self.object.active_ip
        
        active_os = metric_list.metrix_uname['os']
        active_kernel = metric_list.metrix_uname['kernel']

        metrix_netconn = metric_list.metrix_netconn
        metrix_netconn_established = {}
        metrix_netconn_other = {}
        for iter,item in metrix_netconn.items():
            if item['status'] == 'ESTABLISHED':
                metrix_netconn_established.update({iter:item})
            else:
                metrix_netconn_other.update({iter:item})

        metrix_ifaces = metric_list.metrix_netif
        ip_checker = 0
        for name,item in metrix_ifaces.items():
            for key,address in item.items():
                if active_ip == address:
                    ip_checker = 1
        if ip_checker == 0:
            active_ip = "%s does not presented! Please, check it" % (active_ip)

        metrix_proc = metric_list.metrix_proc
        metrix_users = metric_list.metrix_users
        metrix_users_collector = {}
        for pid,name in metrix_users.items():
            pidname = metrix_proc[pid]['name']
            metrix_users_collector.update({pid:[name,pidname]})

        metrix_cpu_5 = []
        metrix_ram_5 = []
        metrix_swap_5 = []
        metrix_date_5 = []
        for metrics in metric_list_5:
            metrix_cpuer = list(map(float, metrics.metrix_cpu.split()))
            metrix_cpu_5.append(metrix_cpuer[0])
            metrix_ram_5.append(metrics.metrix_ram['percent'])
            metrix_swap_5.append(metrics.metrix_swap['percent'])
            metrix_date_5.append(metrics.metrix_created.strftime("%d/%m/%Y, %H:%M:%S"))
        
        metrix_rom_names = []
        metrix_rom_percents = []
        for disks in metric_list.metrix_rom:
            metrix_rom_names.append(disks)
            metrix_rom_percents.append(metric_list.metrix_rom[disks]['percent'])
            
        metric_list_render = {
            'active_name': self.object.active_name,
            'active_token': self.object.active_token,
            'last_metrix_created': metric_list.metrix_created,
            'active_hostname': active_hostname,
            'active_ip': active_ip,
            'active_os': active_os,
            'active_kernel': active_kernel,
            'metrix_cpu_5': metrix_cpu_5,
            'metrix_ram_5': metrix_ram_5,
            'metrix_swap_5': metrix_swap_5,
            'metrix_date_5': metrix_date_5,
            'metrix_rom_names': metrix_rom_names,
            'metrix_rom_percents': metrix_rom_percents,
            'metrix_netconn_established': metrix_netconn_established,
            'metrix_netconn_other': metrix_netconn_other,
            'metrix_ifaces_collector': metrix_ifaces,
            'metrix_users_collector': metrix_users_collector,
            'metrix_proc': metrix_proc,
            'pk': pk,
        }
        return render(request, 'show_active_details.html', 
                      {'metric_list_render': metric_list_render})


class ShowActives(View):
    template_name = 'show_actives.html'

    def get(self, request):
        active_list = Active.objects.all().order_by('active_created')
        last_metrix = Metrix.objects.latest('metrix_created')
        last_active = Active.objects.filter().get(active_token=last_metrix.metrix_token)
        last_active = last_active.active_name
        last_metrix_time = last_metrix.metrix_created
        active_list_render = {}
        iterq = 0
        for active in active_list:
            try:
                metrix = Metrix.objects.filter(metrix_token=active.active_token) \
                                       .order_by('metrix_created').last()
                candidate = {iterq: {
                    'active_name': active.active_name,
                    'active_ip': active.active_ip,
                    'active_hostname': active.active_hostname,
                    'active_metrix_created': metrix.metrix_created,
                    'active_cpu1': metrix.metrix_cpu.split()[0],
                    'active_cpu2': metrix.metrix_cpu.split()[1],
                    'active_cpu3': metrix.metrix_cpu.split()[2],
                    'active_ram_total': metrix.metrix_ram['total'],
                    'active_ram_used': metrix.metrix_ram['used'],
                    'active_ram_percent': metrix.metrix_ram['percent'],
                    'active_swap_total': metrix.metrix_swap['total'],
                    'active_swap_used': metrix.metrix_swap['used'],
                    'active_swap_percent': metrix.metrix_swap['percent'],
                    'active_rom': metrix.metrix_rom,
                    'pk': active.pk,
                }}
                active_list_render.update(candidate)
            except:
                candidate = {iterq: {
                    'active_name': active.active_name,
                    'active_ip': active.active_ip,
                    'active_hostname': active.active_hostname,
                    'active_metrix_created': 'NO DATA',
                    'active_cpu1': 'NO DATA',
                    'active_cpu2': 'NO DATA',
                    'active_cpu3': 'NO DATA',
                    'active_ram_total': 'NO DATA',
                    'active_ram_used': 'NO DATA',
                    'active_ram_percent': 'NO DATA',
                    'active_swap_total': 'NO DATA',
                    'active_swap_used': 'NO DATA',
                    'active_swap_percent': 'NO DATA',
                    'active_rom': 'NO DATA',
                    'pk': active.pk,
                }}
                active_list_render.update(candidate)
            iterq = iterq +1
        active_list_menu = {
            'last_active': last_active, 
            'last_metrix_time': last_metrix_time,
        }
        return render(request, 'show_actives.html', 
                      {'active_list_render': active_list_render, 
                       'active_list_menu': active_list_menu,})
