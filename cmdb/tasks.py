from __future__ import absolute_import
from celery import shared_task
from common.ansible_api import AdHoc
from multiprocessing import current_process
from cmdb.models.Host import Host
from opsplt.settings import JOBID_CHOICE
import random

@shared_task
def host_state(host):
    current_process()._config = {'semprefix': '/mp'}
    jobid = ''.join(random.sample(JOBID_CHOICE,20))
    host_list = [host]
    adhoc = AdHoc(host_list,jobid)
    result = adhoc.run('ping')
    host = Host.objects.get(ipaddress=host)
    host.state = 'up' if 'ping' in result._result.keys() and result._result['ping'] == 'pong' else 'down'
    host.save()
    return result._result

