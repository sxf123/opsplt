from django.conf.urls import url
from application.views.ServiceView import service_list,ServiceAdd,service_exists,service_delete,ServiceUpdate,service_state,service_search,service_log,service_log_list,download_logs

urlpatterns = [
    url(r'^service/list/$',service_list,name='service_list'),
    url(r'^service/add/$',ServiceAdd.as_view(),name='service_add'),
    url(r'^service/exists/$',service_exists,name="service_exists"),
    url(r'^service/delete/$',service_delete,name='service_delete'),
    url(r'^service/update/(?P<id>[0-9]+)/$',ServiceUpdate.as_view(),name='service_update'),
    url(r'^service/state/$',service_state,name='service_state'),
    url(r'^service/log/(?P<id>[0-9]+)/$',service_log,name='service_log'),
    url(r'^service/log_list/$',service_log_list,name='service_log_list'),
    url(r'^service/search/$',service_search,name='service_search'),
    url(r'^service/logs/download/(?P<id>[0-9]+)/(?P<host>(.*))/(?P<logfile>(.*))/$',download_logs,name='download_logs')
]