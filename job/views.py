from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from cmdb.models.Host import Host
from job.tasks import run_playbook
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from opsplt.settings import JOBID_CHOICE
import random
from celery.result import AsyncResult
from job.models import JobResult
from django.views.generic import View
from job.models import Job
import os
from job.models import JobState
import time
from django.contrib.auth.decorators import permission_required

@require_http_methods(["GET"])
@login_required
@permission_required('job.exec_job',raise_exception=True)
def job_execute(request,id):
    job = Job.objects.get(pk=id)
    host = Host.objects.all()
    context = {'host':[{'id':h.ipaddress,'text':h.hostname} for h in host],'job':job}
    return render(request,'job/job_execute.html',context)

@require_http_methods(['POST'])
@login_required
@permission_required('job.exec_job',raise_exception=True)
def ansible_playbook(request):
    job_id = ''.join(random.sample(JOBID_CHOICE,20))
    host_list = request.POST.get('host').split(",")
    playbook_content = request.POST.get('playbook')
    playbook_name = job_id + ".yml"
    playbook = '/opt/ansible-api/{}'.format(playbook_name)
    job_name = request.POST.get('job_name')
    with open(playbook,'w') as f:
        f.write(playbook_content)
        f.close()
    res = run_playbook.delay(host_list,playbook,job_id)
    job_state = JobState(
        jobid=job_id,
        jobname=job_name,
        start_time=time.strftime('%Y-%m-%d %H:%M:%S'),
        state="PENDING"
    )
    job_state.save()
    return JsonResponse({'celery_id':res.id,'job_id':job_id,'host':request.POST.get('host')})

@require_http_methods(['POST'])
@login_required
@permission_required('job.scan_jobresult',raise_exception=True)
def job_result(request):
    jobid = request.POST.get('jobid')
    celeryid = request.POST.get('celeryid')
    host = request.POST.get('host')
    status = AsyncResult(celeryid).status
    if status == 'PENDING':
        result = JobResult.objects.filter(jobid=jobid).filter(host=host).values('jobid','host','task','result','state')
        return JsonResponse({'status':'pending','result':list(result)})
    elif status == 'SUCCESS':
        result = JobResult.objects.filter(jobid=jobid).filter(host=host).values('jobid','host','task','result','state')
        if(os.path.exists('/opt/ansible-api/{}.yml'.format(jobid))):
            os.remove('/opt/ansible-api/{}.yml'.format(jobid))
        job_state = JobState.objects.get(jobid=jobid)
        job_state.stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        job_result = JobResult.objects.filter(jobid=jobid)
        state_list = [jr.state for jr in job_result]
        if "FAILURE" in state_list:
            job_state.state = 'FAILURE'
        else:
            job_state.state = 'SUCCESS'
        job_state.save()
        return JsonResponse({'status':'success','result':list(result)})
    elif status == 'FAILURE':
        if (os.path.exists('/opt/ansible-api/{}.yml'.format(jobid))):
            os.remove('/opt/ansible-api/{}.yml'.format(jobid))
        job_state = JobState.objects.get(jobid=jobid)
        job_state.stop_time = time.strftime('%Y-%m-%d %H:%M:%S')
        job_state.state = "FAILURE"
        job_state.save()
        return JsonResponse({'status':'failure'})



@require_http_methods(["POST"])
@login_required
@permission_required('job.scan_jobresult',raise_exception=True)
def job_exec_result(request):
    celeryid = request.POST.get('celeryid')
    jobid = request.POST.get('jobid')
    host = request.POST.get('host').split(',')
    context = {'celeryid':celeryid,'jobid':jobid,'host':host}
    return render(request,'job/job_result.html',context)

class JobContent(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('job.add_job',raise_exception=True))
    def get(self,request,*args,**kwargs):
        return render(request,'job/job_content.html')
    @method_decorator(login_required)
    @method_decorator(permission_required('job.add_job',raise_exception=True))
    def post(self,request,*args,**kwargs):
        job_name = request.POST.get('job_name');
        job_desc = request.POST.get('job_desc');
        job_type = request.POST.get('job_type');
        job_content = request.POST.get('job_content');
        if job_type == 'python':
            job_name = job_name + ".py"
        elif job_type == "shell":
            job_name = job_name + ".sh"
        elif job_type == "playbook":
            job_name = job_name + ".yaml"
        job = Job(
            job_name = job_name,
            job_desc = job_desc,
            job_type = job_type,
            job_content = job_content
        )
        job.save()
        return JsonResponse({'message':'add job {} success'.format(job_name)})

@require_http_methods(["GET"])
@login_required
@permission_required('job.scan_job',raise_exception=True)
def job_list(request):
    job_list = Job.objects.all()
    context = {'job_list':job_list}
    return render(request,'job/job_list.html',context)

@require_http_methods(["POST"])
@login_required
@permission_required('job.delete_job',raise_exception=True)
def job_delete(request):
    id = request.POST.get('id')
    job = Job.objects.get(pk=id)
    job.delete()
    return JsonResponse({'message':'delete {} success'.format(job.job_name)})

class JobUpdate(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('job.update_job',raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        job = Job.objects.get(pk=id)
        self.context = {'job':job}
        return render(request,'job/job_update.html',self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required('job.update_job',raise_exception=True))
    def post(self,request,*args,**kwargs):
        job_content = request.POST.get('job_content')
        id = kwargs.get('id')
        job = Job.objects.get(pk=id)
        job.job_content = job_content
        job.save()
        return JsonResponse({'message':'update {} success'.format(job.job_name)})

@require_http_methods(["GET"])
@login_required
@permission_required('job.scan_jobstate',raise_exception=True)
def job_history(request):
    job_state = JobState.objects.exclude(state="PENDING")
    context = {'job_state':job_state}
    return render(request,'job/job_history.html',context)

@require_http_methods(["GET"])
@login_required
@permission_required('job.scan_jobresult',raise_exception=True)
def job_history_result(request,jobid):
    host_list = JobResult.objects.filter(jobid=jobid).values('host').distinct()
    for host in host_list:
        state_set = JobResult.objects.filter(jobid=jobid).filter(host=host.get('host'))
        state_list = [s.state for s in state_set]
        if 'FAILURE' in state_list:
            host['state'] = "FAILURE"
        else:
            host['state'] = 'SUCCESS'
    job_result = JobResult.objects.filter(jobid=jobid).filter(host=host_list[0].get('host'))
    context = {'job_result': job_result,'host_list':host_list,'jobid':jobid}
    return render(request,'job/job_history_result.html',context)

@require_http_methods(["POST"])
@login_required
@permission_required('job.scan_jobresult',raise_exception=True)
def job_history_host_result(request):
    host = request.POST.get('host')
    jobid = request.POST.get('jobid')
    jobresult = JobResult.objects.filter(jobid=jobid).filter(host=host)
    return JsonResponse({'jobresult':[{'host':j.host,'task':j.task,'result':j.result,'state':j.state} for j in jobresult]})