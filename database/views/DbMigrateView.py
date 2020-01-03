from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from database.tasks import db_migrate
from database.models import Database
from opsplt.settings import FLYWAY_BASEDIR
import os
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
from database.models import Result


class MigrateView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        database_id = request.POST.get("id")
        database = Database.objects.get(pk=database_id)
        config_file_dir = os.path.join(FLYWAY_BASEDIR,"conf")
        config_file = os.path.join(config_file_dir,"{0}-{1}.conf".format(database.schema_name,database.schema_url))
        res = db_migrate.delay(config_file)
        return JsonResponse({"migrate_id":res.id,"state":res.state})

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(MigrateView,self).dispatch(request,*args,**kwargs)


class MigrateStatusView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        migrate_id = request.POST.get('migrate_id')
        status = AsyncResult(migrate_id).status
        if status == "PENDING":
            response = {"status":"pending"}
        elif status == "FAILURE":
            response = {"status":"failure"}
        elif status == "SUCCESS":
            result = Result.objects.get(migrate_id=migrate_id)
            if result.migrate_status == 0:
                response = {"status":"success","migrate_result":result.migrate_result}
            else:
                response = {"status":"failure","migrate_result":result.migrate_result}
        return JsonResponse(response)

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(MigrateStatusView,self).dispatch(request,*args,**kwargs)

class MigrateResultView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        migrate_id = request.GET.get('migrate_id')
        self.context = {"migrate_id":migrate_id}
        return render(request,'database/migrate_result.html',self.context)
