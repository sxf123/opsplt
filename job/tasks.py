from __future__ import absolute_import
from celery import shared_task
from common.ansible_api import PlayBook
from multiprocessing import current_process
import logging
import traceback

logger = logging.getLogger("default")

@shared_task
def run_playbook(host_list,playbook,extra_vars=None):
    current_process()._config = {'semprefix': '/mp'}
    try:
        playbook_obj = PlayBook(host_list,run_playbook.request.id,extra_vars=extra_vars)
        res = playbook_obj.runPlayBook(playbook)
        return res
    except Exception:
        logger.error("[ERROR] " + traceback.format_exc())

@shared_task
def add(a,b):
    return a + b
