from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from database.models import SqlFile
from datetime import datetime
from database.models import Database
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from opsplt.settings import FLYWAY_BASEDIR
import os
import logging
from django.db.models import Q
import time

logger = logging.getLogger("default")

class SqlFileListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        database_id = kwargs.get("id")
        sql_file_list = SqlFile.objects.filter(database__id=database_id)
        self.context = {"sql_file_list":sql_file_list,'database_id':database_id}
        return render(request,'database/sql_list.html',self.context)

class SqlFileAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        database_id = kwargs.get('id')
        self.context = {"database_id":database_id}
        return render(request,'database/sql_add.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        database_id = kwargs.get('id')
        sql_name = request.POST.get('sql_name')
        sql_content = request.POST.get('sql_content')
        sql_version = str(int(time.mktime(datetime.now().timetuple())))
        database = Database.objects.get(pk=database_id)
        sql_file = SqlFile(
            sql_name = sql_name,
            sql_version = sql_version,
            sql_content = sql_content,
            database = database
        )
        sql_file.save()
        sql_file_name = "V{}__{}.sql".format(sql_version,sql_name)
        sql_file_dir = os.path.join(FLYWAY_BASEDIR,'sql')
        with open(os.path.join(sql_file_dir,sql_file_name),"w") as fp:
            fp.write(sql_content)
            fp.close()
        logger.info("[INFO] write sql file {} success".format(sql_file_name))
        return JsonResponse({"message":"add V{}__{}.sql success".format(sql_version,sql_name)})

class SqlFileUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        sql_file = SqlFile.objects.get(pk=id)
        database_id = sql_file.database.id
        self.context = {"sql_file":sql_file,"database_id":database_id,"sql_file_id":id}
        return render(request,'database/sql_update.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get('id')
        sql_file = SqlFile.objects.get(pk=id)
        sql_content = request.POST.get("sql_content")
        sql_file.sql_content = sql_content
        sql_file.save()
        sql_file_name = "V{}__{}.sql".format(sql_file.sql_version, sql_file.sql_name)
        sql_file_dir = os.path.join(FLYWAY_BASEDIR, 'sql')
        with open(os.path.join(sql_file_dir, sql_file_name), "w") as fp:
            fp.write(sql_content)
            fp.close()
        logger.info("[INFO] write sql file {} success".format(sql_file_name))
        return JsonResponse({"message":"update V{}__{}.sql success".format(sql_file.sql_version,sql_file.sql_name)})

class SqlFileDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        sql_file_id = request.POST.get("id")
        sql_file = SqlFile.objects.get(pk=sql_file_id)
        sql_file.delete()
        # sql_file_name = "V{}__{}.sql".format(sql_file.sql_version,sql_file.sql_name)
        # sql_file_dir = os.path.join(FLYWAY_BASEDIR,'sql')
        # os.remove(os.path.join(sql_file_dir,sql_file_name))
        return JsonResponse({"message":"delete V{}__{}.sql success".format(sql_file.sql_version,sql_file.sql_name)})

class SqlFileExistView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        sql_name = request.POST.get('sql_name')
        sql_version = request.POST.get('sql_version')
        if SqlFile.objects.filter(Q(sql_name=sql_name)).exists():
            result = False
        else:
            result = True
        return JsonResponse(result,safe=False)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SqlFileExistView,self).dispatch(request,*args,**kwargs)