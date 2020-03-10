from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor
from job.models import JobResult
import json

class ResultsCollector(CallbackBase):
	def __init__(self,jobid,*args,**kwargs):
		super(ResultsCollector,self).__init__(*args,**kwargs)
		self.host_ok = {}
		self.host_unreachable = {}
		self.host_failed = {}
		self.jobid = jobid
		self.result = {}

	def v2_runner_on_unreachable(self,result):
		self.result = result
		job_res = {
			'rc': result._result['rc'] if 'rc' in result._result.keys() else '',
			'changed': 'true' if result._result['changed'] else 'false',
			'msg': result._result['msg'] if 'msg' in result._result.keys() else '',
			'cmd': result._result['cmd'] if 'cmd' in result._result.keys() else '',
			'stdout': result._result['stdout'] if 'stdout' in result._result.keys() else '',
			'stderr': result._result['stderr'] if 'stderr' in result._result.keys() else ''
		}
		job_result = JobResult(
			jobid = self.jobid,
			host = result._host,
			task = result._task,
			result = json.dumps(job_res),
			state = "UNREACHABLE",
		)
		job_result.save()

	def v2_runner_on_ok(self,result,*args,**kwargs):
		self.result = result
		job_res = {
			'rc': result._result['rc'] if 'rc' in result._result.keys() else '',
			'changed': result._result['changed'] if 'changed' in result._result.keys() else 'false',
			'msg': result._result['msg'] if 'msg' in result._result.keys() else '',
			'cmd': result._result['cmd'] if 'cmd' in result._result.keys() else '',
			'stdout': result._result['stdout'] if 'stdout' in result._result.keys() else '',
			'stderr': result._result['stderr'] if 'stderr' in result._result.keys() else ''
		}
		job_result = JobResult(
			jobid = self.jobid,
			host = result._host,
			task = result._task,
			result = json.dumps(job_res),
			state = "SUCCESS"
		)
		job_result.save()

	def v2_runner_on_failed(self,result,*args,**kwargs):
		self.result = result
		job_res = {
			'rc': result._result['rc'] if 'rc' in result._result.keys() else '',
			'changed': 'true' if 'changed' in result._result.keys() else 'false',
			'msg': result._result['msg'] if 'msg' in result._result.keys() else '',
			'cmd': result._result['cmd'] if 'cmd' in result._result.keys() else '',
			'stdout': result._result['stdout'] if 'stdout' in result._result.keys() else '',
			'stderr': result._result['stderr'] if 'stderr' in result._result.keys() else ''
		}
		job_result = JobResult(
			jobid = self.jobid,
			host = result._host,
			task = result._task,
			result = json.dumps(job_res),
			state = "FAILURE"
		)
		job_result.save()

class Options:
	def __init__(self,connection=None,module_path=None,forks=None,remote_user=None,private_key_file=None,ssh_common_args=None,ssh_extra_args=None,sftp_extra_args=None,
				scp_extra_args=None,become=None,become_method=None,become_user=None,verbosity=None,check=False,diff=False,
				listhosts=None,listtasks=None,listtags=None,syntax=None,extra_vars=None):
		self.connection = connection
		self.module_path = module_path
		self.forks = forks
		self.remote_user = remote_user
		self.private_key_file = private_key_file
		self.ssh_common_args = ssh_common_args
		self.ssh_extra_args = ssh_extra_args
		self.sftp_extra_args = sftp_extra_args
		self.scp_extra_args = scp_extra_args
		self.become = become
		self.become_method = become_method
		self.become_user = become_user
		self.verbosity = verbosity
		self.check = check
		self.diff = diff
		self.listhosts=listhosts
		self.listtasks=listtasks
		self.listtags=listtags
		self.syntax=syntax
		self.extra_vars = extra_vars


class AdHoc:
	def __init__(self,host_list,jobid,options=None):
		self.host_list = host_list
		self.loader = DataLoader()
		self.options = options or Options(connection='smart',forks=5,remote_user='root',ssh_common_args='-C -o ControlPersist=30s')
		self.passwords = dict()
		self.sources = ','.join(self.host_list)
		if len(self.host_list) == 1:
			self.sources += ','
		self.inventory = InventoryManager(loader=self.loader,sources=self.sources)
		self.variable_manager = VariableManager(loader=self.loader,inventory=self.inventory)
		self.variable_manager.extra_args = self.options.extra_vars
		self.jobid = jobid
	def run(self,module,args=''):
		play_source = dict(
			name = 'Ansible Play',
			hosts = self.host_list,
			gather_facts = 'no',
			tasks=[dict(action=dict(module=module,args=args))]
		)
		play = Play().load(play_source,variable_manager=self.variable_manager,loader=self.loader)
		tqm = None
		callback = ResultsCollector(self.jobid)
		try:
			tqm = TaskQueueManager(
				inventory = self.inventory,
				variable_manager = self.variable_manager,
				loader = self.loader,
				options = self.options,
				passwords = self.passwords
			)
			tqm._stdout_callback = callback
			result = tqm.run(play)
		finally:
			if tqm is not None:
				tqm.cleanup()
		return callback.result

class PlayBook:
	def __init__(self,host_list,jobid,extra_vars=None,options=None):
		self.host_list = host_list
		self.options = options or Options(connection='smart',forks=5,extra_vars=extra_vars)
		self.loader = DataLoader()
		self.sources = ','.join(self.host_list)
		if len(self.host_list) == 1:
			self.sources += ','
		self.inventory = InventoryManager(loader=self.loader,sources = self.sources)
		self.variable_manager = VariableManager(self.loader,inventory=self.inventory)
		self.variable_manager.extra_vars = extra_vars
		self.jobid = jobid
	def runPlayBook(self,playbook):
		playbook = PlaybookExecutor(
			playbooks = [playbook],
			inventory = self.inventory,
			variable_manager = self.variable_manager,
			loader = self.loader,
			options = self.options,
			passwords = None
		)
		callback = ResultsCollector(self.jobid)
		playbook._tqm._stdout_callback = callback
		result = playbook.run()
		return result