from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from job.tasks import run_playbook
from celery.result import AsyncResult
from cmdb.models.Host import Host
from job.models import JobResult
from job.models import JobState
from job.models import Job
import time


class JobExecuteView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    @method_decorator(permission_required('job.exec_job',raise_exception=True))
    def get(self, request, *args, **kwargs):
        job_id = kwargs.get('id')
        job = Job.objects.get(pk=job_id)
        host = Host.objects.all()
        self.context = {'host': [{'id': h.ipaddress, 'text': h.hostname} for h in host], 'job': job}
        return render(request, 'job/job_execute.html', self.context)

    @method_decorator(login_required)
    @method_decorator(permission_required('job.exec_job', raise_exception=True))
    def post(self, request, *args, **kwargs):
        host_list = request.POST.get('host').split(',')
        playbook_content = request.POST.get('playbook')
        job_name = request.POST.get('job_name')
        playbook_name = job_name + ".yml"
        playbook = '/opt/ansible-api/{}'.format(playbook_name)
        with open(playbook, 'w') as f:
            f.write(playbook_content)
            f.close()
        res = run_playbook.delay(host_list, playbook)
        job_state = JobState(
            jobid=res.id,
            jobname=job_name,
            start_time=time.strftime('%Y-%m-%d %H:%M:%S'),
            state="PENDING"
        )
        job_state.save()
        return JsonResponse({'job_id': res.id, 'host': request.POST.get('host')})

class JobResultView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    @method_decorator(permission_required('job.scan_jobresult', raise_exception=True))
    def get(self, request, *args, **kwargs):
        jobid = request.GET.get('jobid')
        host = request.GET.get('host').split(',')
        self.context = {'jobid': jobid, 'host': host}
        return render(request, 'job/job_result.html', self.context)

    @method_decorator(login_required)
    @method_decorator(permission_required('job.scan_jobresult', raise_exception=True))
    def post(self, request, *args, **kwargs):
        jobid = request.POST.get('jobid')
        host = request.POST.get('host')
        status = AsyncResult(jobid).status
        if status == "PENDING":
            result = JobResult.objects.filter(jobid=jobid).filter(host=host).values('jobid','host','task','result','state')
            return JsonResponse({'status': 'pending', 'result': list(result)})
        elif status == "SUCCESS":
            result = JobResult.objects.filter(jobid=jobid).filter(host=host).values('jobid', 'host', 'task', 'result', 'state')
            job_state = JobState.objects.get(jobid=jobid)
            job_state.stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
            job_result = JobResult.objects.filter(jobid=jobid)
            state_list = [jr.state for jr in job_result]
            if "FAILURE" in state_list:
                job_state.state = 'FAILURE'
            else:
                job_state.state = 'SUCCESS'
            job_state.save()
            return JsonResponse({'status': 'success', 'result': list(result)})
        elif status == "FAILURE":
            job_state = JobState.objects.get(jobid=jobid)
            job_state.stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
            job_state.state = "FAILURE"
            job_state.save()
            return JsonResponse({'status': 'failure'})