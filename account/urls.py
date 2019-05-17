from django.conf.urls import url
from account.views import UserAdd,UserUpdate,user_list,user_delete,GroupAdd,GroupUpdate,group_list,group_delete,ChangePassword

urlpatterns = [
    url(r'^user/list/$',user_list,name='user_list'),
    url(r'^user/add/$',UserAdd.as_view(),name='user_add'),
    url(r'^user/update/(?P<id>[0-9]+)/$',UserUpdate.as_view(),name='user_update'),
    url(r'^user/delete/$',user_delete,name='user_delete'),
    url(r'^group/list/$',group_list,name='group_list'),
    url(r'^group/add/$',GroupAdd.as_view(),name='group_add'),
    url(r'^group/update/(?P<id>[0-9]+)/$',GroupUpdate.as_view(),name='group_update'),
    url(r'^group/delete/$',group_delete,name='group_delete'),
    url(r'^user/change-password/$',ChangePassword.as_view(),name='change_password')
]