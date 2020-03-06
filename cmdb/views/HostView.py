from django.shortcuts import render
from django.views.generic import View
from cmdb.models.Host import Host
from cmdb.forms.HostForm import HostAddForm,HostUpdateForm
from cmdb.models.Node import Node
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from opsplt.settings import JOBID_CHOICE
import random
from common.ansible_pass import autocreate_publickey
from opsplt.settings import AES_ENCRYPT_KEY
from common.crypt import encrypt,decrypt
from job.models import JobResult

class HostView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('cmdb.scan_host',raise_exception=True))
    def get(self,request,*args,**kwargs):
        host = Host.objects.all()
        self.context = {'host': host,'host_list':[h.hostname for h in host]}
        return render(request,'cmdb/host/host_list.html',self.context)

class HostAdd(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('cmdb.add_host',raise_exception=True))
    def get(self,request,*args,**kwargs):
        host_add_form = HostAddForm()
        node_list = Node.objects.filter(level=3)
        self.context = {'host_add_form':host_add_form,'node_list':[{'id':n.node_id,'text':'/'.join(get_pid_list(n))} for n in node_list]}
        return render(request,'cmdb/host/host_add.html',self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required('cmdb.add_host',raise_exception=True))
    def post(self,request,*args,**kwargs):
        host_add_form = HostAddForm(request.POST)
        if host_add_form.is_valid():
            hostname = host_add_form.cleaned_data.get('hostname')
            ipaddress = host_add_form.cleaned_data.get('ipaddress')
            password = host_add_form.cleaned_data.get('password')
            hosttype = host_add_form.cleaned_data.get('hosttype')
            cpu_nums = host_add_form.cleaned_data.get('cpu_nums')
            memory = host_add_form.cleaned_data.get('memory')
            disk = host_add_form.cleaned_data.get('disk')
            instance_id = host_add_form.cleaned_data.get('instance_id')
            node = request.POST.getlist('node')
            host = Host(
                hostname = hostname,
                ipaddress = ipaddress,
                password = encrypt(AES_ENCRYPT_KEY,password),
                hosttype = hosttype,
                cpu_nums = cpu_nums,
                memory = memory,
                disk = disk,
                instance_id = instance_id
            )
            host.save()
            for n in node:
                host.node.add(Node.objects.get(node_id=n))
            return HttpResponseRedirect(reverse('host_list'))
        else:
            self.context = {'host_add_form': host_add_form,'errors': host_add_form.errors}
            return render(request,'cmdb/host/host_add.html',self.context)

class HostUpdate(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('cmdb.change_host',raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        host = Host.objects.get(pk=id)
        host_update_form = HostUpdateForm({'hostname':host.hostname,'hostname_hidden':host.hostname,'ipaddress':host.ipaddress,'hosttype':host.hosttype,'cpu_nums':host.cpu_nums,'memory':host.memory,'disk':host.disk,'instance_id':host.instance_id})
        nodes = Node.objects.filter(level=3)
        node_list = [{'id': n.node_id, 'text': '/'.join(get_pid_list(n))} for n in nodes]
        self.context = {'host_update_form': host_update_form,'node_list':node_list,'node_id_list':[n.node_id for n in host.node.all()]}
        return render(request,'cmdb/host/host_update.html',self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required('cmdb.change_host',raise_exception=True))
    def post(self,request,*args,**kwargs):
        host_update_form = HostUpdateForm(request.POST)
        if host_update_form.is_valid():
            id = kwargs.get('id')
            host = Host.objects.get(pk=id)
            host.hostname = host_update_form.cleaned_data.get('hostname_hidden')
            host.ipaddress = host_update_form.cleaned_data.get('ipaddress')
            host.password = encrypt(AES_ENCRYPT_KEY,host_update_form.cleaned_data.get('password'))
            host.hosttype = host_update_form.cleaned_data.get('hosttype')
            host.cpu_nums = host_update_form.cleaned_data.get('cpu_nums')
            host.memory = host_update_form.cleaned_data.get('memory')
            host.disk = host_update_form.cleaned_data.get('disk')
            host.instance_id = host_update_form.cleaned_data.get('instance_id')
            node_list = request.POST.getlist('node')
            host.save()
            nodes = host.node.all()
            for n in nodes:
                host.node.remove(n)
            for n in node_list:
                host.node.add(Node.objects.get(node_id=n))
            return HttpResponseRedirect(reverse('host_list'))
        else:
            self.context = {'host_update_form': host_update_form,'errors': host_update_form.errors}
            return render(request,'cmdb/host/host_update.html',self.context)

@require_http_methods(['POST'])
@login_required
@permission_required('cmdb.delete_host',raise_exception=True)
def delete_host(request):
    id = request.POST.get('id')
    print(type(id))
    host = Host.objects.get(pk=id)
    nodes = host.node.all()
    for n in nodes:
        host.node.remove(n)
    host.delete()
    return JsonResponse({'message':'remove host success'})


@csrf_exempt
@require_http_methods(['POST'])
@login_required
@permission_required('cmdb.scan_host',raise_exception=True)
def host_exist(request):
    hostname = request.POST.get('hostname')
    host = Host.objects.filter(hostname=hostname)
    if host.exists():
        return JsonResponse(False,safe=False)
    else:
        return JsonResponse(True,safe=False)

def get_pid_list(node):
    node_list = []
    if node.level == 0:
        return node_list.append(node.name)
    else:
        node_list.append(node.name)
        for i in range(node.level):
            node_parent = Node.objects.get(node_id=node.node_pid)
            node_list.append(node_parent.name)
            node = node_parent
    return reversed(node_list)

@require_http_methods(["GET"])
@login_required
@permission_required('cmdb.scan_host',raise_exception=True)
def host_detail(request,hostname):
    hostname = hostname
    host = Host.objects.get(hostname=hostname)
    nodes = host.node.all()
    context = {"host":host,'nodes':['/'.join(get_pid_list(node)) for node in nodes]}
    return render(request,'cmdb/host/host_detail.html',context)

@require_http_methods(['POST'])
@login_required
def host_status(request):
    hostname = request.POST.get('hostname')
    host = Host.objects.get(hostname=hostname)
    state = host.state
    return JsonResponse({'host':hostname,'state':state})

@require_http_methods(['POST'])
@login_required
def generate_publickey(request):
    hostname = request.POST.get('hostname')
    host = Host.objects.get(hostname=hostname)
    jobid = ''.join(random.sample(JOBID_CHOICE,20))
    password = decrypt(AES_ENCRYPT_KEY,host.password)
    res = autocreate_publickey([host.ipaddress],password,jobid)
    jobstate = JobResult.objects.get(jobid=jobid).state
    return JsonResponse({'result':res._result,'state':jobstate})
