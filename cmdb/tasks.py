from __future__ import absolute_import
from celery import shared_task
from common.ansible_ping import ping
from multiprocessing import current_process
from cmdb.models.Host import Host

@shared_task
def host_state(host):
    current_process()._config = {'semprefix': '/mp'}
    host_list = [host]
    result = ping(host_list)
    host = Host.objects.get(ipaddress=host)
    host.state = 'up' if 'ping' in result.keys() and result['ping'] == 'pong' else 'down'
    host.save()
    return result

