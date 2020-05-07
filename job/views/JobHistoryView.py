from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from job.models import JobState
from job.models import JobResult
from django.http import JsonResponse

class JobHistoryList(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('job.scan_jobstate',raise_exception=True))
    def get(self, request, *args, **kwargs):
        job_state = JobState.objects.exclude(state="PENDING")
        self.context = {'job_state': job_state}
        return render(request, 'job/job_history.html', self.context)

class JobHistoryResultView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('job.scan_jobresult',raise_exception=True))
    def get(self, request, *args, **kwargs):
        jobid = kwargs.get('jobid')
        host_list = JobResult.objects.filter(jobid=jobid).values('host').distinct()
        for host in host_list:
            state_set = JobResult.objects.filter(jobid=jobid).filter(host=host.get('host'))
            state_list = [s.state for s in state_set]
            if 'FAILURE' in state_list:
                host['state'] = "FAILURE"
            else:
                host['state'] = 'SUCCESS'
        job_result = JobResult.objects.filter(jobid=jobid).filter(host=host_list[0].get('host'))
        context = {'job_result': job_result, 'host_list': host_list, 'jobid': jobid, "tasks": [jr.id for jr in job_result]}
        return render(request, 'job/job_history_result.html', context)

    @method_decorator(login_required)
    @method_decorator(permission_required('job.scan_jobresult',raise_exception=True))
    def post(self,request,*args,**kwargs):
        host = request.POST.get('host')
        jobid = kwargs.get('jobid')
        jobresult = JobResult.objects.filter(jobid=jobid).filter(host=host)
        return JsonResponse({'jobresult': [{'host': j.host, 'task': j.task, 'result': j.result, 'state': j.state} for j in jobresult]})