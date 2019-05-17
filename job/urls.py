from django.conf.urls import url
from job.views import job_execute,ansible_playbook,job_result,job_exec_result,JobContent,job_list,job_delete,JobUpdate,job_history,job_history_result,job_history_host_result

urlpatterns = [
    url(r'^execute/(?P<id>[0-9]+)/$',job_execute,name='job_execute'),
    url(r'^ansible-playbook/$',ansible_playbook,name='ansible_playbook'),
    url(r'^result/$',job_result,name='job_result'),
    url(r'^exec/result/$',job_exec_result,name='job_exec_result'),
    url(r'^content/$',JobContent.as_view(),name='job_content'),
    url(r'^list/$',job_list,name='job_list'),
    url(r'^delete/$',job_delete,name='job_delete'),
    url(r'^update/(?P<id>[0-9]+)/$',JobUpdate.as_view(),name='job_update'),
    url(r'^history/$',job_history,name='job_history'),
    url(r'^history-result/(?P<jobid>(.*))/$',job_history_result,name='job_history_result'),
    url(r'history/host/result/$',job_history_host_result,name='job_history_host_result')
]