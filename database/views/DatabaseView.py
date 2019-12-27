from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from database.models import Database
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from common.crypt import encrypt,decrypt
from opsplt.settings import AES_ENCRYPT_KEY
from django.http import JsonResponse
from database.tasks import database_init
from opsplt.settings import FLYWAY_BASEDIR
import os
import logging

logger = logging.getLogger("default")

class DatabaseListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        database_list = Database.objects.all()
        self.context = {"database_list":database_list}
        return render(request, "database/database_list.html", context=self.context)

class DatabaseAddView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        env_dict = {"dev":"开发环境","test":"测试环境","release":"预发环境","prod":"生产环境","custom":"客户环境"}
        self.context = {'env_dict': env_dict}
        return render(request,'database/database_add.html',self.context)

    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        schema_name = request.POST.get('schema_name')
        schema_url = request.POST.get('schema_url')
        schema_username = request.POST.get('schema_username')
        schema_password = request.POST.get('schema_password')
        schema_env = request.POST.get('schema_env')
        database = Database(
            schema_name=schema_name,
            schema_url=schema_url,
            schema_username=schema_username,
            schema_password=encrypt(AES_ENCRYPT_KEY,schema_password),
            schema_env=schema_env
        )
        database_init.delay(schema_name,schema_url,schema_username,schema_password)
        database.save()
        return HttpResponseRedirect(reverse('database_list'))

class DatabaseUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        database = Database.objects.get(pk=id)
        schema_password = decrypt(AES_ENCRYPT_KEY,database.schema_password)
        env_dict = {"dev": "开发环境", "test": "测试环境", "release": "预发环境", "prod": "生产环境", "custom": "客户环境"}
        self.context = {'database':database,'schema_password':schema_password,"env_dict":env_dict}
        return render(request,'database/database_update.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get('id')
        database = Database.objects.get(pk=id)
        database.schema_name = request.POST.get('schema_name')
        database.schema_url = request.POST.get('schema_url')
        database.schema_username = request.POST.get('schema_username')
        database.schema_password = encrypt(AES_ENCRYPT_KEY,request.POST.get('schema_password'))
        database.schema_env = request.POST.get('schema_env')
        database.save()
        return HttpResponseRedirect(reverse('database_list'))

class DatabaseDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = request.POST.get('id')
        database = Database.objects.get(pk=id)
        database.delete()
        config_dir = os.path.join(FLYWAY_BASEDIR,"conf/{}-{}.conf".format(database.schema_name,database.schema_url))
        os.remove(config_dir)
        logger.info('[INFO] delete {} success'.format(config_dir))
        return JsonResponse({"message":"delete {} success".format(database.schema_name)})

class DatabaseSearchView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        schema_name = request.POST.get('schema_name')
        database_list = Database.objects.filter(schema_name__contains=schema_name)
        if database_list.exists():
            database_res = [{"id":database.id,"schema_name":database.schema_name,"schema_url":database.schema_url,"schema_env":database.schema_env} for database in database_list]
        else:
            database_res = []
        return JsonResponse({"database_list":database_res})
