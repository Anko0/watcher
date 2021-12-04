import os
import psutil
import re
import requests
import json
import asyncio

from datetime import datetime


def collector():
    cpu = ''
    cpus = psutil.cpu_count()
    for x in psutil.getloadavg():
        cpu += "%s " % (round(x / cpus * 100, 2))

    rammer = psutil.virtual_memory()
    ram = {'total': rammer[0], 'percent': rammer[2], 'used': rammer[3], 
           'free': rammer[4], 'buffers': rammer[7], 'cached': rammer[8]}

    swapper = psutil.swap_memory()
    swap = {'total': swapper[0], 'used': swapper[1], 
            'free': swapper[2], 'percent': swapper[3]}

    partitions = str(psutil.disk_partitions())
    rom = {}
    repartitions = re.findall("mountpoint='(.+?)',", partitions)
    for part in repartitions: 
        rommer = psutil.disk_usage(part)
        rom_updater = {part:{'total':rommer[0], 'used': rommer[1], 
                             'free': rommer[2], 'percent': rommer[3]}}
        rom.update(rom_updater)

    procs = {proc.pid: proc.info for proc in psutil.process_iter(['name', 'username'])}

    conner = psutil.net_connections(kind='inet')
    conn = {}
    iter = 0
    for x in conner:
        try:
            conn_updater = {iter: {'laddr': x[3][0], 'lport': x[3][1], 'raddr': x[4][0],
                                   'rport': x[4][1], 'status': x[5], 'pid': x[6]}}
            conn.update(conn_updater)
        except:
            conn_updater = {iter: {'laddr': x[3][0], 'lport': x[3][1], 'raddr': '', 
                                   'rport': '', 'status': x[5], 'pid': x[6]}}
            conn.update(conn_updater)
        iter = iter + 1

    nwifer1 = psutil.net_if_addrs()
    metrix_ifaces_collector = {}
    for y1 in nwifer1:
        renwif1 = re.findall("address='(.+?)',", str(nwifer1[y1]))
        metrix_ifaces_collector.update({y1:{'ipv4': '', 'ipv6': '', 'mac': ''}})
        for address in renwif1:
            if re.match("^\d+[.]\d+[.]\d+[.]\d+$", address):
                metrix_ifaces_collector[y1]['ipv4'] = address
            elif re.match("^.{2}[:].{2}[:].{2}[:].{2}[:].{2}[:].{2}$", address):
                metrix_ifaces_collector[y1]['mac'] = address
            else:
                metrix_ifaces_collector[y1]['ipv6'] = address

    unamer = str(os.uname())
    uname_os = re.findall("sysname='(.+?)',", unamer)
    uname_kernel = re.findall("release='(.+?)',", unamer)
    uname_hostname = re.findall("nodename='(.+?)',", unamer)
    uname = {'os': uname_os, 'kernel': uname_kernel, 'hostname': uname_hostname}

    userser = psutil.users()
    users = {}
    for z in userser:
        users_updater = {z[4]: z[0]}
        users.update(users_updater)

    created = str(datetime.now())

    headers = {'Content-type': 'application/json'}
    metrix = {'metrix_token': active_token, 'metrix_created': created,
              'metrix_cpu': cpu, 'metrix_ram': ram, 'metrix_swap': swap, 
              'metrix_rom': rom, 'metrix_proc': procs, 'metrix_netconn': conn, 
              'metrix_netif': metrix_ifaces_collector, 'metrix_uname': uname, 
              'metrix_users': users}
    json_data = json.dumps(metrix)
    response = requests.post(api_url, data=json_data, headers=headers)
    print(response.status_code, response.reason)


async def main():
    print("Started at", datetime.now())
    while(1):
        await asyncio.gather(
            asyncio.to_thread(collector),
            asyncio.sleep(time_delay))


with open('watcher_agent.json', 'r') as f:
    config = json.load(f)
active_token = config['ACTIVE_TOKEN']
api_url = config['API_URL']
time_delay = config['TIME_DELAY']

asyncio.run(main())

