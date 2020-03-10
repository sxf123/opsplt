from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import JsonResponse
from job.models import Job

class JobListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('job.scan_job', raise_exception=True))
    def get(self, request, *args, **kwargs):
        job_list = Job.objects.all()
        self.context = {'job_list':job_list}
        return render(request, 'job/job_list.html', self.context)

class JobAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('job.add_job',raise_exception=True))
    def get(self,request,*args,**kwargs):
        return render(request,'job/job_content.html')
    @method_decorator(login_required)
    @method_decorator(permission_required('job.add_job',raise_exception=True))
    def post(self,request,*args,**kwargs):
        job_name = request.POST.get('job_name')
        job_desc = request.POST.get('job_desc')
        job_type = request.POST.get('job_type')
        job_content = request.POST.get('job_content')
        extra_vars = request.POST.get('extra_vars')
        if job_type == 'python':
            job_name = job_name + ".py"
        elif job_type == "shell":
            job_name = job_name + ".sh"
        elif job_type == "playbook":
            job_name = job_name + ".yaml"
        job = Job(
            job_name=job_name,
            job_desc=job_desc,
            job_type=job_type,
            job_content=job_content,
            extra_vars=extra_vars
        )
        job.save()
        return JsonResponse({'message': 'add job {} success'.format(job_name)})

class JobUpdateView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    @method_decorator(permission_required('job.update_job', raise_exception=True))
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        job = Job.objects.get(pk=id)
        self.context = {'job': job}
        return render(request, 'job/job_update.html', self.context)

    @method_decorator(login_required)
    @method_decorator(permission_required('job.update_job', raise_exception=True))
    def post(self, request, *args, **kwargs):
        job_content = request.POST.get('job_content')
        extra_vars = request.POST.get('extra_vars')
        id = kwargs.get('id')
        job = Job.objects.get(pk=id)
        job.job_content = job_content
        job.extra_vars = extra_vars
        job.save()
        return JsonResponse({"message": "update {} success".format(job.job_name)})

class JobDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('job.delete_job', raise_exception=True))
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        job = Job.objects.get(pk=id)
        job.delete()
        return JsonResponse({'message':'delete {} success'.format(job.job_name)})

