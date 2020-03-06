from django.conf.urls import url
from consul_manage.views.ConsulView import ConsulListView
from consul_manage.views.ConsulView import ConsulAddView
from consul_manage.views.ConsulView import ConsulUpdateView
from consul_manage.views.ConsulView import ConsulDeleteView
from consul_manage.views.ConfigView import ConsulConfigListView
from consul_manage.views.ConfigView import ConsulConfigUpdateView
from consul_manage.views.ConfigView import ConsulConfigSaveView

urlpatterns = [
    url(r"^list/$",ConsulListView.as_view(),name='consul_list'),
    url(r'^add/$',ConsulAddView.as_view(),name='consul_add'),
    url(r'^update/(?P<id>[0-9]+)/$',ConsulUpdateView.as_view(),name='consul_update'),
    url(r'^delete/$',ConsulDeleteView.as_view(),name='consul_delete'),
    url(r'^config/list/(?P<id>[0-9]+)/$',ConsulConfigListView.as_view(),name='consul_config_list'),
    url(r'^config/kv/(?P<id>[0-9]+)/$',ConsulConfigUpdateView.as_view(),name='consul_config_kv'),
    url(r'^config/save/$',ConsulConfigSaveView.as_view(),name='config_consul_kv_save')
]