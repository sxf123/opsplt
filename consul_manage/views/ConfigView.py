from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from consul_manage.models import ConsulStatus
from common.consul_config import get_key_value
from common.consul_config import list_key
from django.http import JsonResponse
from common.consul_config import put_key_value
import chardet

class ConsulConfigListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        consul = ConsulStatus.objects.get(pk=id)
        key_list = list_key(consul.address,consul.port)
        key_dict = [{"key_name":key,"custom":consul.custom} for key in key_list]
        self.context = {'key_dict':key_dict,'config_id':id}
        return render(request,'consul_manage/config_list.html',self.context)

class ConsulConfigUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        consul = ConsulStatus.objects.get(pk=id)
        key = request.GET.get("key")
        value = get_key_value(consul.address,consul.port,key)
        self.context = {"value":value,'key':key,'service':key.split('/')[1],'config_id':id}
        return render(request,'consul_manage/config_kv.html',self.context)

class ConsulConfigSaveView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = request.POST.get('id')
        consul = ConsulStatus.objects.get(pk=id)
        key = request.POST.get('key')
        value = request.POST.get('value')
        put_key_value(consul.address,consul.port,key,value.encode('utf-8'))
        return JsonResponse({"message":"put key {} success".format(key)})

