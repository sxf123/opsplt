from django.views.generic import View
from django.utils.decorators import method_decorator
from cmdb.serializers import NodeTreeSerializer
from cmdb.models.Node import Node
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_GET
from django.http.response import JsonResponse
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

@require_GET
@login_required
@permission_required('cmdb.scan_node',raise_exception=True)
def cluster_tree(request):
    return render(request,'cmdb/cluster/cluster_tree.html')

class NodeTreeView(View):
    def __init__(self):
        self.context = {}

    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_node",raise_exception=True))
    def get(self,request,*args,**kwargs):
        nodes = Node.objects.filter(parent=None)
        serializer = NodeTreeSerializer(nodes,many=True)
        self.context = {"node":serializer.data}
        return JsonResponse(data=self.context,safe=False)

class NodeListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.scan_node",raise_exception=True))
    def get(self,request,*args,**kwargs):
        nodes = Node.objects.all()
        self.context = {"nodes":nodes}
        return render(request,"cmdb/cluster/node_list.html",self.context)

class NodeAddView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_node",raise_exception=True))
    def get(self,request,*args,**kwargs):
        nodes_select = Node.objects.filter(level__in=[0,1,2])
        self.context = {"nodes_select":[{"id":node.id,"text":node.name} for node in nodes_select]}
        return render(request,"cmdb/cluster/node_add.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.add_node",raise_exception=True))
    def post(self,request,*args,**kwargs):
        name = request.POST.get("name")
        parent = request.POST.get("parent")
        Node.objects.create(name=name,parent=Node.objects.get(pk=parent))
        return HttpResponseRedirect(reverse('node_list'))

class NodeUpdateView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_node",raise_exception=True))
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        node = Node.objects.get(pk=id)
        nodes_select = [{"id":node.id,"text":node.name} for node in Node.objects.filter(level__in=[0,1,2])]
        self.context = {'node':node,'nodes_select':nodes_select}
        return render(request,"cmdb/cluster/node_update.html",self.context)
    @method_decorator(login_required)
    @method_decorator(permission_required("cmdb.change_node",raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = kwargs.get("id")
        name = request.POST.get("name")
        parent = request.POST.get("parent")
        node = Node.objects.get(pk=id)
        node.name = name
        node.parent = Node.objects.get(pk=parent)
        node.save()
        return HttpResponseRedirect(reverse("node_list"))

class HostNodeListView(View):
    def __init__(self):
        self.context = {}
    @method_decorator(login_required)
    @method_decorator(permission_required('cmdb.scan_host',raise_exception=True))
    def post(self,request,*args,**kwargs):
        id = request.POST.get("id")
        node = Node.objects.get(pk=id)
        host = node.host_set.all()
        return JsonResponse({'host': [{'hostname': h.hostname, 'ipaddress': h.ipaddress, 'hosttype': h.hosttype, 'cpu_nums': h.cpu_nums,'memory': h.memory, 'disk': h.disk} for h in host]})





