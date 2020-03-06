from django.conf.urls import url
from cmdbapi.views.HostView import HostDetailView
from cmdbapi.views.HostView import HostUpdateView
from cmdbapi.views.HostView import HostTestView

urlpatterns = [
    url(r'^host/detail$',HostDetailView.as_view(),name='host_detail_api'),
    url(r'^host/update$',HostUpdateView.as_view(),name='host_update_api'),
    url(r'^host/test$',HostTestView.as_view(),name='host_test_api')
]