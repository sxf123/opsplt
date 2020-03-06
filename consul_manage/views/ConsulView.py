from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from consul_manage.models import ConsulStatus
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse

class ConsulListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        consul_list = ConsulStatus.objects.all()
        self.context = {"consul_list":consul_list}
        return render(request,'consul_manage/consul_list.html',self.context)

class ConsulAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        return render(request,'consul_manage/consul_add.html')
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        consul_address = request.POST.get('address')
        consul_port = request.POST.get('port')
        consul_custom = request.POST.get('custom')
        consul = ConsulStatus(
            address=consul_address,
            port=consul_port,
            custom=consul_custom,
            status=0
        )
        consul.save()
        return HttpResponseRedirect(reverse('consul_list'))

class ConsulUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        consul = ConsulStatus.objects.get(pk=id)
        self.context = {'consul_manage':consul}
        return render(request,'consul_manage/consul_update.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get('id')
        consul = ConsulStatus.objects.get(pk=id)
        address = request.POST.get('address')
        port = request.POST.get('port')
        custom = request.POST.get('custom')
        consul.address = address
        consul.port = port
        consul.custom = custom
        consul.save()
        return HttpResponseRedirect(reverse('consul_list'))

class ConsulDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = request.POST.get("id")
        consul = ConsulStatus.objects.get(pk=id)
        consul.delete()
        return JsonResponse({"message":"delete {}'s consul_manage success".format(consul.custom)})
