from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.http import require_http_methods
from application.models.Service import Service
from application.forms import ServiceAddForm,ServiceUpdateForm
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cmdb.models.Node import Node
import requests
import json
from common.ansible_api import AdHoc
from opsplt.settings import JOBID_CHOICE
import random
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
import os
from django.contrib.auth.decorators import permission_required

@require_http_methods(['GET'])
@login_required
@permission_required('application.scan_service',raise_exception=True)
def service_list(request):
    service_list = Service.objects.all()
    context = {'service_list':service_list,'service_dict':list(service_list.values('name','port','product'))}
    return render(request,'application/service/service_list.html',context)

class ServiceAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('application.add_service',raise_exception=True))
    def get(self,request,*args,**kwargs):
        service_add_form = ServiceAddForm()
        self.context = {'service_add_form':service_add_form}
        return render(request,'application/service/service_add.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        service_add_form = ServiceAddForm(request.POST)
        if service_add_form.is_valid():
            name = service_add_form.cleaned_data.get('name')
            desc = service_add_form.cleaned_data.get('desc')
            port = service_add_form.cleaned_data.get('port')
            log_dir = service_add_form.cleaned_data.get('log_dir')
            product = request.POST.get('product')
            service = Service(
                name =name,
                desc = desc,
                port = port,
                log_dir = log_dir,
                product = product
            )
            service.save()
            return HttpResponseRedirect(reverse('service_list'))
        else:
            self.context = {'service_add_form':service_add_form,'errors':service_add_form.errors}
            return render(request,'application/service/service_add.html',self.context)

@require_http_methods(['POST'])
@csrf_exempt
@login_required
@permission_required('application.scan_service',raise_exception=True)
def service_exists(request):
    name = request.POST.get('name')
    service = Service.objects.filter(name=name)
    if service.exists():
        return JsonResponse(False,safe=False)
    else:
        return JsonResponse(True,safe=False)

@require_http_methods(['POST'])
@login_required
@permission_required('application.delete_service',raise_exception=True)
def service_delete(request):
    id = request.POST.get('id')
    service = Service.objects.get(pk=id)
    service.delete()
    return JsonResponse({'message':'delete service {} success'.format(service.name)})

class ServiceUpdate(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('application.change_service',raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        service = Service.objects.get(pk=id)
        service_update_form = ServiceUpdateForm(model_to_dict(service))
        self.context = {'service_update_form':service_update_form,'service':service}
        return render(request,'application/service/service_update.html',self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required('application.change_service', raise_exception=True))
    def post(self,request,*args,**kwargs):
        service_update_form = ServiceUpdateForm(request.POST)
        if service_update_form.is_valid():
            id = kwargs.get('id')
            service = Service.objects.get(pk=id)
            service.name = service_update_form.cleaned_data.get('name')
            service.desc = service_update_form.cleaned_data.get('desc')
            service.port = service_update_form.cleaned_data.get('port')
            service.log_dir = service_update_form.cleaned_data.get('log_dir')
            service.product = request.POST.get('product')
            service.save()
            return HttpResponseRedirect(reverse('service_list'))
        else:
            self.context = {'service_update_form':service_update_form,'errors':service_update_form.errors}
            render(request,'application/service/service_update.html',self.context)

@require_http_methods(['POST'])
@csrf_exempt
@permission_required('application.scan_service',raise_exception=True)
def service_state(request):
    name = request.POST.get('name')
    service = Service.objects.get(name=name)
    node = Node.objects.get(name=name)
    host = node.host_set.all()
    state_list = []
    for h in host:
        state = 'UP' if get_state(h.ipaddress,service.port) == 1 else 'DOWN'
        state_list.append({'name':service.name,'host':h.hostname,'state':state})
    return JsonResponse(state_list,safe=False)

def get_state(ip,port):
    url = 'http://{}:{}/actuator/health'.format(ip,port)
    try:
        req = requests.get(url,timeout=2)
        if req.status_code == 200:
            if json.loads(req.content)['status'] == 'UP':
                return 1
            else:
                return 0
        else:
            return 0
    except Exception as e:
        return 0

@require_http_methods(['POST'])
@login_required
@permission_required('application.scan_service',raise_exception=True)
def service_search(request):
    name = request.POST.get('name')
    service = list(Service.objects.filter(name=name).values('id','name','desc','port','product'))
    context = {'service':service}
    return JsonResponse(context)

@require_http_methods(['POST'])
@login_required
@permission_required('application.download_log',raise_exception=True)
def service_log_list(request):
    id = request.POST.get('id')
    host = request.POST.get('host')
    service = Service.objects.get(pk=id)
    log_dir = service.log_dir
    host_list = [host]
    job_id = ''.join(random.sample(JOBID_CHOICE, 20))
    adhoc = AdHoc(host_list,job_id)
    result = adhoc.run('shell','ls {}'.format(log_dir))
    context = {'result':["{}/{}".format(log_dir,f) for f in result._result['stdout'].split('\n')]}
    return JsonResponse(context,safe=False)


@require_http_methods(['GET'])
@login_required
@permission_required('application.download_log',raise_exception=True)
def service_log(request,id):
    service = Service.objects.get(pk=id)
    node = Node.objects.get(name=service.name)
    host_list = [h.ipaddress for h in node.host_set.all()]
    context = {'id':id,'host_list':host_list}
    return render(request,'application/service/service_log.html',context)

@require_http_methods(["GET"])
@login_required
@permission_required('application.download_log',raise_exception=True)
def download_logs(request,id,host,logfile):
    service = Service.objects.get(pk=id)
    filename = '/data/applogs/{}{}/{}'.format(host, service.log_dir, logfile)
    host_list = [host]
    job_id = ''.join(random.sample(JOBID_CHOICE, 20))
    adhoc = AdHoc(host_list, job_id)
    adhoc.run('fetch', 'src={}/{} dest=/data/applogs'.format(service.log_dir, logfile))
    file = open(filename,'rb')
    response = StreamingHttpResponse(file)
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename={}".format(escape_uri_path(logfile))
    return response