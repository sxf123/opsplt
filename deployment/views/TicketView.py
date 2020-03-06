from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from deployment.models import Ticket
from deployment.models import Project
from opsplt.settings import JOBID_CHOICE
import random
from django.http import JsonResponse

class TicketListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        ticket_list = Ticket.objects.all()
        self.context = {"ticket_list":ticket_list}
        return render(request,'deployment/ticket/ticket_list.html',self.context)

class TicketAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        project_list = Project.objects.all()
        projects = [{"id":project.project_name,"text":project.project_name} for project in project_list]
        self.context = {"project_list":projects}
        return render(request,'deployment/ticket/ticket_add.html',self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        deploy_title = request.POST.get("deploy_title")
        project = request.POST.get("project")
        sql_content = request.POST.get("sql_content")
        config_content = request.POST.get("config_content")
        ticket_no = ''.join(random.sample(JOBID_CHOICE,10))
        ticket = Ticket(
            ticket_no=ticket_no,
            deploy_title=deploy_title,
            project=project,
            sql_content=sql_content,
            config_content=config_content
        )
        ticket.save()
        return JsonResponse({"message":"commit ticket {} success".format(ticket_no)})

class TicketDetailView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        ticket_no = request.GET.get("ticket_no")
        ticket = Ticket.objects.get(ticket_no=ticket_no)
        self.context = {"ticket":ticket}
        return render(request,"deployment/ticket/ticket_detail.html",self.context)

class TicketSqlAndConfigView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        type = request.GET.get("type")
        ticket_no = request.GET.get("ticket_no")
        ticket = Ticket.objects.get(ticket_no=ticket_no)
        self.context = {"ticket": ticket}
        if type == "sql":
            return render(request,"deployment/ticket/ticket_sql.html",self.context)
        elif type == "config":
            return render(request,"deployment/ticket/ticket_config.html",self.context)

