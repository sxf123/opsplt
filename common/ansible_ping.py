from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from .ansible_api import Options
from ansible import constants as C

class ResultCollector(CallbackBase):
    def __init__(self,*args,**kwargs):
        super(ResultCollector,self).__init__(*args,**kwargs)
        self.result = {}
    def v2_runner_on_unreachable(self,result):
        self.result = result._result
    def v2_runner_on_ok(self,result,*args,**kwargs):
        self.result = result._result
    def v2_runner_on_failed(self,result,*args,**kwargs):
        self.result = result._result

def ping(host_list):
    C.HOST_KEY_CHECKING = False
    loader = DataLoader()
    options = Options(connection='smart',forks=5,remote_user='root',ssh_common_args='-C -o ControlPersist=30s')
    passwords = dict()
    sources = host_list[0] + ','
    inventory = InventoryManager(loader=loader,sources=sources)
    variable_manager = VariableManager(loader=loader,inventory=inventory)
    play_source = dict(
        name = 'Test Ping',
        hosts = host_list,
        gather_facts = 'no',
        tasks = [dict(action=dict(module='ping',args=''))]
    )
    play = Play().load(play_source,variable_manager=variable_manager,loader=loader)
    tqm = None
    callback = ResultCollector()
    try:
        tqm = TaskQueueManager(
            inventory = inventory,
            variable_manager = variable_manager,
            loader = loader,
            options = options,
            passwords = passwords
        )
        tqm._stdout_callback = callback
        res = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()
    return callback.result