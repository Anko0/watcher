from .models import Active, Metrix


class ActiveMetrix():

    def get_metrix(active_pk):
        current_active = Active.objects.filter().get(pk=active_pk)

        try: 
            metric_list = Metrix.objects.filter(metrix_token=current_active.active_token) \
                                        .latest('metrix_created')
        except:
            return 1
        metric_list_5 = Metrix.objects.filter(metrix_token=current_active.active_token) \
                                        .order_by('-metrix_created')[:15:-1] 

        active_hostname = current_active.active_hostname
        if active_hostname != metric_list.metrix_uname['hostname'][0]:
            active_hostname = "%s is wrong! Real hostname is %s" % \
                                (active_hostname, metric_list.metrix_uname['hostname'][0])
        active_ip = current_active.active_ip
            
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
            try:
                pidname = metrix_proc[pid]['name']
            except:
                pidname = '?'
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
            'active_name': current_active.active_name,
            'active_token': current_active.active_token,
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
            'pk': active_pk,
        }
        return metric_list_render


class ConectedActives():

    def last_connected():
        try:
            last_metrix = Metrix.objects.latest('metrix_created')
        except:
            active_list_menu = {
                'last_active': '-', 
                'last_metrix_time': '-',
            }
            return active_list_menu
        last_active = Active.objects.filter().get(active_token=last_metrix.metrix_token)
        last_active = last_active.active_name
        last_metrix_time = last_metrix.metrix_created
        active_list_menu = {
                'last_active': last_active, 
                'last_metrix_time': last_metrix_time,
            }
        return active_list_menu

    def list_connected():
        active_list = Active.objects.all().order_by('active_created')
        if len(active_list) == 0:
            return 1
        active_list_render = {}
        iterq = 0
        for active in active_list:
            try:
                metrix = Metrix.objects.filter(metrix_token=active.active_token) \
                                        .order_by('metrix_created').last()
                candidate = {
                    iterq: {
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
                    }
                }
            except:
                candidate = {
                    iterq: {
                        'active_name': active.active_name,
                        'active_ip': active.active_ip,
                        'active_hostname': active.active_hostname,
                        'active_metrix_created': 'NO DATA',
                        'active_cpu1': 'NO DATA',
                        'active_cpu2': 'NO DATA',
                        'active_cpu3': 'NO DATA',
                        'active_ram_total': 'NO DATA',
                        'active_swap_total': 'NO DATA',
                        'active_rom': 'NO DATA',
                        'pk': active.pk,
                    }
                }
            active_list_render.update(candidate)
            iterq = iterq + 1
        return active_list_render