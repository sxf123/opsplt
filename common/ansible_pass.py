from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from collections import namedtuple
from ansible.inventory.host import Host
from ansible import constants as C
from common.ansible_api import ResultsCollector
from common.ansible_api import Options


def autocreate_publickey(host_list,password,jobid):
    C.HOST_KEY_CHECKING = False
    loader = DataLoader()
    options = Options(connection='smart',forks=5,ssh_common_args='-C -o ControlPersist=30s')
    passwords = dict()
    if len(host_list) <= 1:
        sources = host_list[0] + ','
    else:
        sources = ','.join(host_list)
    inventory = InventoryManager(loader=loader,sources=sources)
    variable_manager = VariableManager(loader=loader,inventory=inventory)
    for host in host_list:
        host_info = Host(name=host,port=22)
        variable_manager.set_host_variable(host_info,'ansible_ssh_user','root')
        variable_manager.set_host_variable(host_info,'ansible_ssh_pass',password)
    play_source = dict(
        name = 'Generate Publickey',
        hosts = host_list,
        gather_facts = 'no',
        tasks = [dict(action=dict(module='authorized_key',args=dict(user='root',key="{{ lookup('file','/root/.ssh/id_rsa.pub') }}")))]
    )
    play = Play().load(play_source,variable_manager=variable_manager,loader=loader)
    tqm = None
    callback = ResultsCollector(jobid)
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords
        )
        tqm._stdout_callback = callback
        result = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()
    return callback.result


