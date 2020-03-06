from django.views.generic import View
from django.shortcuts import render
from deployment.models import Project
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class ProjectListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        project_list = Project.objects.all()
        self.context = {"project_list":project_list}
        return render(request,"deployment/project/project_list.html",self.context)

class ProjectAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        return render(request,"deployment/project/project_add.html")
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        project_name = request.POST.get("project_name")
        project_git_url = request.POST.get("project_git_url")
        project_port = request.POST.get("project_port")
        project = Project(
            project_name=project_name,
            project_git_url=project_git_url,
            project_port=project_port
        )
        project.save()
        return HttpResponseRedirect(reverse("project_list"))

class ProjectUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        project = Project.objects.get(pk=id)
        self.context = {"project":project}
        return render(request,"deployment/project/project_update.html",self.context)
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        project = Project.objects.get(pk=id)
        project_name = request.POST.get("project_name")
        project_git_url = request.POST.get("project_git_url")
        project_port = request.POST.get("project_port")
        project.project_name = project_name
        project.project_git_url = project_git_url
        project.project_port = project_port
        project.save()
        return HttpResponseRedirect(reverse("project_list"))

class ProjectDeleteView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        id = request.POST.get("id")
        project = Project.objects.get(pk=id)
        project.delete()
        return JsonResponse({"message":"delete {} success".format(project.project_name)})

class ProjectSearchView(View):
    def __init__(self):
        self.context = {}
    # @method_decorator(login_required)
    def post(self,request,*args,**kwargs):
        project_name = request.POST.get("project_name")
        project_list = Project.objects.filter(project_name__contains=project_name)
        if project_list.exists():
            project_res = [{"id":project.id,"project_name":project.project_name,"project_git_url":project.project_git_url,"project_port":project.project_port,"create_time":project.create_time.strftime("%Y-%m-%d"),"update_time":project.update_time.strftime("%Y-%m-%d")} for project in project_list]
        else:
            project_res = []
        return JsonResponse({"project_list":project_res})
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectSearchView, self).dispatch(request,*args,**kwargs)