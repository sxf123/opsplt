from django.shortcuts import render
from cmdb.models.Node import Node
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

@require_http_methods(['GET'])
@login_required
@permission_required('cmdb.scan_node',raise_exception=True)
def tree(request):
    nodes = Node.objects.all()
    context = {"node":[{'id':n.node_id,'pId':n.node_pid,'name':n.name} for n in nodes]}
    return render(request, 'cmdb/cluster/cluster_tree.html', context)


@require_http_methods(['POST'])
@login_required
@permission_required('cmdb.update_node',raise_exception=True)
def update_node(request):
    node_id = request.POST.get('id')
    name = request.POST.get('name')
    node = Node.objects.get(node_id=node_id)
    node.name = name
    node.save()
    return JsonResponse({'message':'edit success'})

@require_http_methods(['POST'])
@login_required
@permission_required('cmdb.add_node',raise_exception=True)
def add_node(request):
    node_id = request.POST.get('id')
    name = request.POST.get('name')
    node_pid = request.POST.get('pid')
    level = request.POST.get('level')
    node = Node(
        node_id = node_id,
        node_pid = node_pid,
        name = name,
        level = level
    )
    node.save()
    return JsonResponse({'message':'add success'})

@require_http_methods(['POST'])
@login_required
@permission_required('cmdb.delete_node',raise_exception=True)
def delete_node(request):
    node_id = request.POST.get('id')
    node = Node.objects.get(node_id=node_id)
    host = node.host_set.all()
    for h in host:
        node.host_set.remove(h)
    node.delete()
    return JsonResponse({'message':'delete success'})

@require_http_methods(['POST'])
@login_required
def delete_multiple_node(request):
    node_id_list = request.POST.getlist('id_list')
    for id in node_id_list:
        node = Node.objects.get(node_id=id)
        node.delete()
    return JsonResponse({'message':'delete multiple success'})

@require_http_methods(['POST'])
@login_required
def get_host_list(request):
    node_id = request.POST.get('id')
    node = Node.objects.get(node_id=node_id)
    host = node.host_set.all()
    return JsonResponse({'host':[{'hostname':h.hostname,'ipaddress':h.ipaddress,'hosttype':h.hosttype,'cpu_nums':h.cpu_nums,'memory':h.memory,'disk':h.disk} for h in host]})

