from django.conf.urls import url
from cmdb.views.HostView import HostView,HostAdd,host_exist,HostUpdate,delete_host,host_detail,host_status
from cmdb.views.TreeView import tree,update_node,add_node,delete_node,delete_multiple_node,get_host_list

urlpatterns = [
    url(r'^host/list/$',HostView.as_view(),name='host_list'),
    url(r'^host/add/$',HostAdd.as_view(),name='host_add'),
    url(r'^host/update/(?P<id>[0-9]+)/$',HostUpdate.as_view(),name='host_update'),
    url(r'^host/delete/$',delete_host,name='host_delete'),
    url(r'^host/exists/$',host_exist,name="host_exist"),
    url(r'^host/detail/(?P<hostname>(.*))/$',host_detail,name='host_detail'),
    url(r'^tree/$',tree,name='cluster_tree'),
    url(r'^update/node/$',update_node,name='update_ztree'),
    url(r'^add/node/$',add_node,name='add_ztree'),
    url(r'^delete/node/$',delete_node,name='delete_ztree'),
    url(r'^delete/multiple/node/$',delete_multiple_node,name='delete_multiple_node'),
    url(r'^host/node/list/$',get_host_list,name='get_node_host_list'),
    url(r'^host/status/$',host_status,name='host_status')
]