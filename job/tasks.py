from __future__ import absolute_import
from celery import shared_task
from common.ansible_api import PlayBook
from multiprocessing import current_process
import logging

logger = logging.getLogger("default")

@shared_task
def run_playbook(host_list,playbook):
    current_process()._config = {'semprefix': '/mp'}
    playbook_obj = PlayBook(host_list,run_playbook.request.id)
    res = playbook_obj.runPlayBook(playbook)
    return res

@shared_task
def add(a,b):
    return a + b
