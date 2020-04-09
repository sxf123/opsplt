from django.conf.urls import url
from cmdb.views.HostView import HostView,HostAdd,host_exist,HostUpdate,delete_host,host_detail,host_status,generate_publickey
from cmdb.views.TreeView import NodeTreeView
from cmdb.views.TreeView import cluster_tree
from cmdb.views.TreeView import NodeListView
from cmdb.views.TreeView import NodeAddView
from cmdb.views.TreeView import NodeUpdateView
from cmdb.views.TreeView import HostNodeListView


urlpatterns = [
    url(r'^host/list/$',HostView.as_view(),name='host_list'),
    url(r'^host/add/$',HostAdd.as_view(),name='host_add'),
    url(r'^host/update/(?P<id>[0-9]+)/$',HostUpdate.as_view(),name='host_update'),
    url(r'^host/delete/$',delete_host,name='host_delete'),
    url(r'^host/exists/$',host_exist,name="host_exist"),
    url(r'^host/detail/(?P<hostname>(.*))/$',host_detail,name='host_detail'),
    url(r'^host/status/$',host_status,name='host_status'),
    url(r'^host/generate/publickey/$',generate_publickey,name='generate_publickey'),
    url(r'^host/node/list/$',HostNodeListView.as_view(),name='host_node_list'),
    url(r'^tree/$',cluster_tree,name='cluster_tree'),
    url(r'^node/tree/$',NodeTreeView.as_view(),name='node_tree'),
    url(r'^node/list/$',NodeListView.as_view(),name='node_list'),
    url(r'^node/add/$',NodeAddView.as_view(),name='node_add'),
    url(r'^node/update/(?P<id>[0-9]+)/$',NodeUpdateView.as_view(),name='node_update')
]